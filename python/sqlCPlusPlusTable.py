#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusCommon

class SQLCPlusPlusTable (sqlCPlusPlusCommon.SQLCPlusPlusCommon):
	#TODO: Add safe functions for parsing data BEFORE database entry (rather than setting element directly)
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							(	#One constructor
								#Parameters
								(
									("pqxx::connection *", "connection",),
								),
								#Args
								(
									("dbquery::DBResult", ("connection",),),
								),
							),
							(	#Two constructor
								#Parameters
								(
									("pqxx::connection *", "connection",),
									("const {primaryKeyType}", "{primaryKey}"),
								),
								#Args
								(
									("dbquery::DBResult", ("connection",),),
									("{primaryKey}", ("{primaryKey}",),),
								),
							),
							#(	#Three constructor  - Templated
							#	#Parameters
							#	),
							#	#Args
							#	(
							#	),
							#),
						)
	#TODO: Expand on this idea and make engine functions
	TEMPLATED_CONSTRUCTOR_ARGS	=	(	#Only One constructor
										#Parameters
										(
											("pqxx::connection *", "connection",),
										),
										#Args
										(
											("dbquery::DBResult", ("connection",),),
										),
									)

	#Schema templates - (ret, functionNametemplate, arguments)
	TABLE_FUNCTION_TEMPLATES =	(
									("void", "selectRowSQL",	(
																	("pqxx::work &", "txn"),
																),
	"""
	pqxx::result res = txn.exec(SQL_SELECT + " {primaryKey} = " + txn.quote({primaryKey}) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
{DBSafeUtilsColumns}
	}}
	"""
									),
									("void", "deleteRowSQL",	(
																	("pqxx::work &", "txn"),
																),
	"""
	pqxx::result res = txn.exec("DELETE FROM \\
		{tableName} \\
	WHERE \\
		{primaryKey} = " + txn.quote({primaryKey}) + \\
	";");
	"""
									),
									("void", "updateRowSQL",	(
																	("pqxx::work &", "txn"),
																),
"""
	pqxx::result res = txn.exec("UPDATE \\
		{tableName} \\
	SET \\
{updateSetColumnList} \\
	WHERE \\
		{primaryKey} = " + txn.quote({primaryKey}) + \\
	";");
"""
									),
									("void", "insertRowSQL",	(
																	("pqxx::work &", "txn"),
																),
"""
	pqxx::result res = txn.parameterized(\"SELECT * FROM {insertStoredProc}\"){insertStoredProcParams}.exec();
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
		dbquery::DBSafeUtils::safeToInt(&this->{primaryKey}, res[i][\"{insertStoredProc}\"]);
	}}
"""
									),
								)
	#Column Functions
	COLUMN_FUNCTION_TEMPLATES =	(
									("{columnType}", "get{columnNameTitle}",	(
																	("void", ""),
																),
	"""	return {columnName};"""
									),
									("void", "set{columnNameTitle}",	(
																	("{columnType}", "{columnName}"),
																),
	"""	{columnName} = {columnName};
	//TODO: Need to add this to the dbTransaction class as an update
	"""
									),
								)

	#Typedef mapping
	TYPEDEFS =	(
					("shared_ptr<{className}>", "p{className}"),
					("vector < p{className} >", "ap{className}"),
					("shared_ptr < ap{className}>", "pap{className}"),
				)

	def __init__(self, outputObject, filename):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__init__(self, outputObject, filename)
		self.dataDict = None


	def __del__(self):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__del__(self)


	def tableFullName(self):
		return self.outputObject.getFullName()

	def tableName(self):
		return self.outputObject.getName()

	def schemaName(self):
		return self.outputObject.getSchemaNameCPP()

	def buildContents(self):
		return str()

	SQL_SELECT = """\"SELECT {columNames} FROM {tableName} WHERE\""""


	def initialiseDataStructuresTable(self):
		self.dataDict = 	{
						"columNames"		:	", ".join("{column}".format(column = columnName) for columnName, columnObj in self.outputObject.getColumns().iteritems()),
						"tableName"			:	self.tableFullName(),
						"primaryKey"		:	self.outputObject.getPrimaryKey(),
						"primaryKeyType" 	:	self.outputObject.getPrimaryKeyType(),
					}
		#Default placeholder for initialising the data
		self.addStaticVariable(self.PUBLIC, "string", "SQL_SELECT", self.SQL_SELECT.format(**self.dataDict)) # Add the class specific constant string
		pass

	#Typedef
	def typedefListHPP(self, className):
		val = str()
		for typedefDetails in self.TYPEDEFS:
			val += self.fmt_typedef(knownType = typedefDetails[0].format(className = className), customType = typedefDetails[1].format(className = className))
		return val

	#Variables
	def classVariableListHPP(self):
		val = "\tpublic:\n"
		for columnName, columnObj in self.outputObject.getColumns().iteritems():
			val += self.classVariableHPP(variableType = columnObj.getType(), variableName = columnObj.getName())
		return val

	# Header
	def tableConstructorHPP (self, className, templatedFunctions, usePrimaryKey):
		parameters = list() # (type, value)
		#Build a list using the constructors defined
		for params in templatedFunctions[0]:
			parameters.append(params)
		#Setup dictionary to use
		columnDictionary = None
		if (True == usePrimaryKey):
			columnDictionary = self.outputObject.getNonPrimaryKeyColums()
			logging.debug("tableConstructorHPP columnDictionary use PK: %s", columnDictionary)
		else:
			columnDictionary = self.outputObject.getColumns()
			logging.debug("tableConstructorHPP columnDictionary non PK: %s", columnDictionary)
		#Add in the table columns
		for columnName, columnObj in columnDictionary.iteritems():
			#TODO: Move this SQL->CPP type conversion into a different place (i.e in columns)
			parameters.append( (self.SQLDATATYPEMAPPING.get(columnObj.getType(), self.SQLDATATYPEDEFAULT)+ " &", columnName) )
		#Output the Complete string
		val = str()
		val += self.constructorHPP(className, parameters, self.dataDict)
		return val

	def templatedColumnFunctionHPP (self, templateFunctions):
		val = str()
		#Build Dict
		for functionDetails in templateFunctions:
			for columnName, columnData in self.outputObject.getColumns().iteritems():
				templateDict = {
					'columnNameTitle'			:	columnName.title(),
					'columnName'				:	columnName,
					'columnType'				:	columnData.getCPPReferenceType(),
					'DBSafeUtilsType'			:	columnData.getCPPSafeType(),
				}
				val += self.classFunctionTemplateHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], templateDict = templateDict )
		return val



	# 	Class HPP: functions : (scope, name, argument(s))
	def buildTableClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.staticVariableHPP()
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS, self.dataDict)
		ret += self.tableConstructorHPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS, True)
		ret += self.tableConstructorHPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS, False)
		ret += self.destructorHPP(className)
		#Functions
		ret += self.functionListHPP(self.TABLE_FUNCTION_TEMPLATES)
		ret += self.templatedColumnFunctionHPP(self.COLUMN_FUNCTION_TEMPLATES)
		#Variables
		##TODO: Remove this and use the generic classScopeVariableHPP instead (with type swaps upfront)
		ret += self.classVariableListHPP()
		ret += "};\n"
		return ret

	# -----------------------------------
	# Implementation
	def tableConstructorCPP (self, className, templatedFunctions, usePrimaryKey):
		parameters = list() # (type, value)
		constructionArgs = list() # (variable, (value,),)
		#Build a list using the constructors defined
		for params in templatedFunctions[0]:
			parameters.append( params )
		for construction in templatedFunctions[1]:
			constructionArgs.append( construction )
		#Setup dictionary to use
		columnDictionary = None
		if (True == usePrimaryKey):
			columnDictionary = self.outputObject.getNonPrimaryKeyColums()
		else:
			columnDictionary = self.outputObject.getColumns()
		#Add in the table columns
		for columnName, columnObj in columnDictionary.iteritems():
			#TODO: Move this SQL->CPP type conversion into a different place (i.e in columns)
			parameters.append( (self.SQLDATATYPEMAPPING.get(columnObj.getType(), self.SQLDATATYPEDEFAULT)+ " &", columnName) )
			constructionArgs.append( (columnName, (columnName,),) )
		#Output the Complete string
		val = str()
		val += self.constructorCPP(className, parameters, constructionArgs, self.dataDict)
		return val

	def updateSetColumnList(self):
		#("{typeof} {name}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (typeof, name,) in parameters)
		columns = list()
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			if columnName != self.outputObject.getPrimaryKey():
				columns.append( "\t\t{column}  = \" + txn.quote({column}) + \"".format(column = columnName) )
		return  ", \\\n".join(columns)

	def columnList(self):
		return ", \\\n\t\t".join(self.outputObject.getColumns().keys())

	#INSERT SQL statements
	#	TODO: Add a specific PK key (asssumes id at present)
	def insertStoredProc(self):
		return "{schemaName}.pIns{tableName}".format(schemaName = self.outputObject.getSchemaNameSQL(), tableName = self.outputObject.getName())

	def insertStoredProcParams(self):
		columns = list()
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			if columnName != self.outputObject.getPrimaryKey():
				columns.append( "(txn.quote({column}))".format(column = columnName) )
		return  "".join(columns)

	#	Templated Table Functions
	def templatedNamedFunctionCPP (self, className, templateFunctions):
		val = str()
		#Build Dict
		templateDict = {
			'tableName'					:	self.outputObject.getFullName(),
			'insertStoredProc'			:	self.insertStoredProc(),
			'insertStoredProcParams'	:	self.insertStoredProcParams(),
			'primaryKey'				:	self.outputObject.getPrimaryKey(),
			'updateSetColumnList'		:	self.updateSetColumnList(),
			'columnList'				:	self.columnList(),
			'DBSafeUtilsColumns'		:	self.getTypeConversion(self.outputObject, "this->"),
		}
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = templateDict )
		return val

	#	Templated Column Functions
	def templatedColumnFunctionCPP (self, className, templateFunctions):
		val = str()
		#Build Dict
		for functionDetails in templateFunctions:
			for columnName, columnData in self.outputObject.getColumns().iteritems():
				templateDict = {
					'columnNameTitle'			:	columnName.title(),
					'columnName'				:	columnName,
					'columnType'				:	columnData.getCPPReferenceType(),
					'DBSafeUtilsType'			:	columnData.getCPPSafeType(),
				}
				val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = templateDict )
		return val


	# 	Class CPP: functions : (scope, name, argument(s))
	def buildTableClassCPP(self, className):
		ret = str()
		ret += self.staticVariableCPP(className)
		ret += self.constructorListCPP(className, self.CONSTRUCTOR_ARGS, self.dataDict)
		ret += self.tableConstructorCPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS, True)
		ret += self.tableConstructorCPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS, False)
		ret += self.destructorCPP(className)
		# Make Function implementations
		ret += self.templatedNamedFunctionCPP(className, self.TABLE_FUNCTION_TEMPLATES)
		ret += self.templatedColumnFunctionCPP(className, self.COLUMN_FUNCTION_TEMPLATES)
		return ret
