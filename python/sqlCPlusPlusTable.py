#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusTable (sqlCPlusPlusBase.SQLCPlusPlusBase):
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							(	#One constructor
								#Parameters
								(
									("dbquery::DBConnection *", "connection",),
								),
								#Args
								(
									("dbquery::DBResult", ("connection",),),
								),
							),
							(	#Two constructor
								#Parameters
								(
									("dbquery::DBConnection *", "connection",),
									("const int", "primaryKey"),
								),
								#Args
								(
									("dbquery::DBResult", ("connection","primaryKey",),),
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
											("dbquery::DBConnection *", "connection",),
										),
										#Args
										(
											("dbquery::DBResult", ("connection",),),
										),
									)

	#Schema templates - (ret, functionNametemplate, arguments)
	TABLE_FUNCTION_TEMPLATES =	(
									("void", "selectRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																),
	"""
	pqxx::result res = txn->exec("SELECT \\
		{columnList} \\
	FROM \\
		{tableName} \\
	WHERE \\
		{primaryKey} = " + txn->quote(pk) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
{safeDataColumn}
	}}
	"""
									),
									("void", "deleteRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																),
	"""
	pqxx::result res = txn->exec("DELETE FROM \\
		{tableName} \\
	WHERE \\
		{primaryKey} = " + txn->quote({primaryKey}) + \\
	";");
	"""
									),
									("void", "updateRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																),
"""
	pqxx::result res = txn->exec("UPDATE \\
		{tableName} \\
	SET \\
{updateSetColumnList} \\
	WHERE \\
		{primaryKey} = " + txn->quote({primaryKey}) + \\
	";");
"""
									),
									("void", "insertRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																),
"""
	pqxx::result res = txn->parameterized(\"{insertStoredProc}\"){insertStoredProcParams}.exec();
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
		dbquery::DBSafeUtils::safeToInt(&this->pk, res[i][\"{insertStoredProc}\"]);
	}}
"""
									),
								)

	TYPEDEFS =	(
					("shared_ptr<{className}>", "p{className}"),
					("vector < p{className} >", "ap{className}"),
					("shared_ptr < ap{className}>", "pap{className}"),
				)

	def __init__(self, outputObject, filename):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.outputObject = outputObject


	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def tableFullName(self):
		return self.outputObject.getFullName()

	def tableName(self):
		return self.outputObject.getName()

	def schemaName(self):
		return self.outputObject.getSchemaName()

	def buildContents(self):
		return str()


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
	def tableConstructorHPP (self, className, templatedFunctions):
		parameters = list() # (type, value)
		#Build a list using the constructors defined
		for params in templatedFunctions[0]:
			parameters.append(params)
		#Add in the table columns
		for columnName, columnObj in self.outputObject.getNonPrimaryKeyColums().iteritems():
			#TODO: Move this SQL->CPP type conversion into a different place (i.e in columns)
			parameters.append( (self.SQLDATATYPEMAPPING.get(columnObj.getType(), self.SQLDATATYPEDEFAULT)+ " &", columnName) )
		#Output the Complete string
		val = "\tpublic:\n"
		val += "\t\t{className} ({parameters});\n".format(className = className, parameters = self.functionArgs(parameters))
		return val



	# 	Class HPP: functions : (scope, name, argument(s))
	def buildTableClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.staticVariableHPP()
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		ret += self.tableConstructorHPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS)
		ret += self.destructorListHPP(className)
		#Functions
		ret += self.functionListHPP(self.TABLE_FUNCTION_TEMPLATES)
		#Variables
		##TODO: Remove this and use the generic classScopeVariableHPP instead (with type swaps upfront)
		ret += self.classVariableListHPP()
		ret += "};\n"
		return ret

	# -----------------------------------
	# Implementation
	def tableConstructorCPP (self, className, templatedFunctions):
		parameters = list() # (type, value)
		constructionArgs = list() # (variable, (value,),)
		#Build a list using the constructors defined
		for params in templatedFunctions[0]:
			parameters.append( params )
		for construction in templatedFunctions[1]:
			constructionArgs.append( construction )
		#Add in the table columns
		for columnName, columnObj in self.outputObject.getNonPrimaryKeyColums().iteritems():
			#TODO: Move this SQL->CPP type conversion into a different place (i.e in columns)
			parameters.append( (self.SQLDATATYPEMAPPING.get(columnObj.getType(), self.SQLDATATYPEDEFAULT)+ " &", columnName) )
			constructionArgs.append( (columnName, (columnName,),) )
		#Output the Complete string
		val = "\tpublic:\n"
		val += "{className}::{className} ({parameters}):\n\t{init}\n{{\n}}\n\n".format(className = className, parameters = self.functionArgs(parameters), init = self.constructorBuilder(constructionArgs))
		return val

	def updateSetColumnList(self):
		#("{typeof} {name}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (typeof, name,) in parameters)
		columns = list()
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			if columnName != self.outputObject.getPrimaryKey():
				columns.append( "\t\t{column}  = \" + txn->quote({column}) + \"".format(column = columnName) )
		return  ", \\\n".join(columns)

	def columnList(self):
		return ", \\\n\t\t".join(self.outputObject.getColumns().keys())

	def getSafeTypeConversion(self):
		val = str()
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			logging.info("getSafeTypeConversion column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\tdbquery::DBSafeUtils::safeTo{datatype}(&this->{column}, res[i][\"{column}\"]);\n".format(column = columnName, datatype = columnData.getCPPType())
		return val

	#INSERT SQL statements
	#	TODO: Add a specific PK key (asssumes id at present)
	def insertStoredProc(self):
		return "{schemaName}.pIns{tableName}".format(schemaName = self.outputObject.getSchemaName(), tableName = self.outputObject.getName())

	def insertStoredProcParams(self):
		columns = list()
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			if columnName != self.outputObject.getPrimaryKey():
				columns.append( "(txn->quote({column}))".format(column = columnName) )
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
			'safeDataColumn'			:	self.getSafeTypeConversion(),
		}
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = templateDict )
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListCPP(self, className):
		val = str()
		val += self.templatedNamedFunctionCPP(className, self.TABLE_FUNCTION_TEMPLATES)
		return val


	# 	Class CPP: functions : (scope, name, argument(s))
	def buildTableClassCPP(self, className):
		ret = str()
		ret += self.staticVariableCPP(className)
		ret += self.constructorListCPP(className, self.CONSTRUCTOR_ARGS)
		ret += self.tableConstructorCPP(className, self.TEMPLATED_CONSTRUCTOR_ARGS)
		ret += self.destructorListCPP(className)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className)
		return ret
