#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusCommon

class SQLCPlusPlusSchema (sqlCPlusPlusCommon.SQLCPlusPlusCommon):
	#Dictionary helper definition
	CONST_TABLENAME 		= 'tableName'
	#Special codes for use in functions to use a table generator function
	CONST_INSERTCOLUMNS		= 'CONST_INSERTCOLUMNS'
	CONST_ALLCOLUMNS		= 'CONST_ALLCOLUMNS'
	CONST_COLUMNTYPE		= 'CONST_COLUMN_TYPE'
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							#One constructor
							(
								#Parameters
								(
									("const string &", "connection",),
								),
								#Args
								(
									("dbquery::DBConnection", ("connection",),),
								),
							),
						)

	# Functions:
	#	1	-	Function for all fields (including PK)
	#	2	-	Primary Key lookup (DONE - primaryKey)
	#	3	-	Insertion function (uses all elements that are not PK) (DONE - CONST_INSERTCOLUMNS)
	#	4	-	Generic WHERE lookup function (data agnostic) (all fields)
	#	5	-	For each foreign Key -
	#				Lookup function by key
	SCHEMA_FUNCTION_TEMPLATES =	(
									("p{tableName}", "get{tableName}", (
																			(CONST_ALLCOLUMNS, ""),
																		),
	"""	p{tableName} obj(new {tableName}(getDBConnection(), {AllColumns}) );
	//Store Object by Primary key
	{tableName}Map[obj->id] = obj;
	transaction.addInsertElement(obj);
	//Return object
	return obj;""",
									),
									("p{tableName}", "g{tableName}", (
																			(CONST_COLUMNTYPE, "primaryKey"),
																		),
	"""//Attempt to find the object
	map{tableName}::iterator it = {tableName}Map.find(primaryKey);
	p{tableName} ptr_{tableName};
	// If cannot be found in cache, create a new object
	if (it == {tableName}Map.end())
	{{
		p{tableName} obj(new {tableName}(getDBConnection(), primaryKey) );
		//Check data exists
		if (obj->selectRow() == true)
		{{
			obj->selectRow();
			//Store Object by Primary key
			{tableName}Map[obj->{primaryKey}] = obj;
			//Copy pointer to return
			ptr_{tableName} = obj;
		}}
	}}
	//Found object, return that
	//TODO: What if data does not exist in DB?
	else
	{{
		//Set return value as second
		ptr_{tableName} = it->second;
	}}
	return ptr_{tableName};""",
									),
									("p{tableName}", "insert{tableName}", (
																			(CONST_INSERTCOLUMNS, ""), #TODO: Run selects inline
																		),
	"""	p{tableName} obj(new {tableName}(getDBConnection(), {NonPKColumns}) );
	//Store Object by Primary key
	{tableName}Map[obj->id] = obj;	//TODO: Fix this! id is not always the PK
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	transaction.addInsertElement(obj);
	//Return object
	return obj;""",
									),
									("pap{tableName}", "getMultiple{tableName}", (
																			("string &", "sqlWhereClause"),
																		),
	"""//Get objects to return
	pap{tableName} objects;
	//Get new transaction
	shared_ptr<pqxx::work> txn = transaction.newTransaction();
	//Build the SQL statement
	string sql = {tableName}::SQL_SELECT + sqlWhereClause + ";";
	// Run the query
	pqxx::result res = txn->exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
		//Local variables for the data
{DBSafeUtilsColumnDefinitions}
		//Set the data
{DBSafeUtilsColumns}
		//Build the actual object
		p{tableName} ptr_{tableName} = get{tableName}({DBSafeUtilsColumnVariables});
		//Store in returned list
		objects->push_back(ptr_{tableName});

	}}
	//Return objects
	return objects;""",
									),
								)

	def __init__(self, outputObject, extension):
		filename = outputObject.getSchemaName() + extension
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__init__(self, outputObject, filename)


	def __del__(self):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__del__(self)


	def schemaName(self):
		return self.outputObject.getSchemaName()


	#Complex Data structure Builder
	def schemaInitialiseDataStructures(self):
		# Override this class
		logging.error("schemaInitialiseDataStructures not overridden")
		pass

	def tableInitialiseDataStructures(self, tableName, tableObj):
		#Table specific building
		# Override this class
		logging.error("tableInitialiseDataStructures not overridden")
		pass

	def initialiseDataStructures(self):
		#Initialse the schema data
		self.schemaInitialiseDataStructures()
		#Use to build the internal structures for building using an engine
		for tableName, tableObj in self.outputObject.tables.iteritems():
			self.tableInitialiseDataStructures(tableName, tableObj)
		pass


	# Overridden class for building
	def buildContents(self):
		return str()


	#Get Table Includes
	def getTableIncludes(self):
		ret = str()
		for tableName, tableObj in self.outputObject.tables.iteritems():
			ret += self.fmt_include(tableObj.getName() + ".hpp")
		return ret

	#TODO: Generate a object creation function - using the object initialiser
	#TODO: Generate functions for each column independently - fetches the rows(s) of data with that parameter (requires the constant SQL query prefix)

	# ---- Header ----
	# Table Column Expander
	def getTableNonPKColumsFunctionArguments(self, tableObject):
		#TODO: implement this to return the list of table objects as a list
		ret = list()
		for columnName, columnObject in tableObject.getNonPrimaryKeyColums().iteritems():
			logging.debug("getTableNonPKColumsFunctionArguments columnName %s", columnName)
			argType = self.SQLDATATYPEMAPPING.get(columnObject.getType(), self.SQLDATATYPEDEFAULT)
			ret.append( (argType, columnObject.getName()) )
		return ret

	#TODO: Merge these
	def getTableAllColumsFunctionArguments(self, tableObject):
		ret = list()
		for columnName, columnObject in tableObject.getColumns().iteritems():
			argType = self.SQLDATATYPEMAPPING.get(columnObject.getType(), self.SQLDATATYPEDEFAULT)
			ret.append( (argType, columnObject.getName()) )
		return ret

	#	Templated Table Functions
	# Templated HPP function List
	def templatedTableFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		#1: Iterate over tables
		for tableName, tableObj in self.outputObject.tables.iteritems():
			templateDict =	{
					self.CONST_TABLENAME	:	tableObj.getName(),
					"NonPKColumns" 			:	tableObj.getNonPKColumnList(),
				}
			#2: Iterate over functions
			for functionDetails in templateFunctions:
				returnValue = functionDetails[0]
				functionName = functionDetails[1]
				args = (())
				# Handle special arguments (first parameter is the CONST_TABLEVARS)
				logging.debug("functionDetails Argument %s", functionDetails[2][0][0])
				if (self.CONST_INSERTCOLUMNS == functionDetails[2][0][0]):
					#Expand the arguments to the table parameters to allow insert
					arguments = self.getTableNonPKColumsFunctionArguments(tableObj)
				elif (self.CONST_ALLCOLUMNS == functionDetails[2][0][0]):
					#Expand the arguments to the table parameters to all columns
					arguments = self.getTableAllColumsFunctionArguments(tableObj)
				else:
					arguments = functionDetails[2]
				logging.info("Arguments %s", arguments)
				#3: Build templated stuff sensibly
				#Process the actual functions
				val += self.classFunctionTemplateHPP(returnValue, functionName, arguments, templateDict)
		return val

	# 	Class HPP: functions : (scope, name, argument(s))
	def buildSchemaClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		ret += self.destructorHPP(className)
		# Make functions
		ret += self.templatedTableFunctionListHPP(self.SCHEMA_FUNCTION_TEMPLATES)
		#TODO: Add function generator for new rows (not primary key driven)
		# Add Scoped variables
		ret += self.classScopeVariableHPP()
		ret += "};\n"
		return ret

	# ---- Implementation ----
	def getSafeTypeVariables(self, tableObject):
		val = str()
		for columnName, columnData in tableObject.getColumns().iteritems():
			logging.debug("getSafeTypeVariables column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\t{datatype} {column};\n".format(column = columnName, datatype = columnData.getCPPReferenceType())
		return val

	# Templated CPP function List
	def templatedTableFunctionListCPP(self, className, templateFunctions):
		val = str()
		#1: Iterate over tables
		for tableName, tableObj in self.outputObject.tables.iteritems():
			templateDict =	{
								self.CONST_TABLENAME			:	tableObj.getName(),
								"AllColumns"					:	tableObj.getAllColumnList(),
								"NonPKColumns" 					:	tableObj.getNonPKColumnList(),
								"DBSafeUtilsColumns"			:	self.getSafeTypeConversion(tableObj),
								"DBSafeUtilsColumnDefinitions" 	:	self.getSafeTypeVariables(tableObj),
								"DBSafeUtilsColumnVariables" 	:	tableObj.getAllColumnList(),
								"primaryKey" 					:	tableObj.getPrimaryKey(),
							}
			#2: Iterate over functions
			for functionDetails in templateFunctions:
				returnValue = functionDetails[0]
				functionName = functionDetails[1]
				args = (())
				implementation = functionDetails[3]
				# Handle special arguments (first parameter is the CONST_TABLEVARS)
				logging.debug("functionDetails Argument %s", functionDetails[2][0][0])
				if (self.CONST_INSERTCOLUMNS == functionDetails[2][0][0]):
					#Expand the arguments to the table parameters to allow insert
					arguments = self.getTableNonPKColumsFunctionArguments(tableObj)
				elif (self.CONST_ALLCOLUMNS == functionDetails[2][0][0]):
					#Expand the arguments to the table parameters to all columns
					arguments = self.getTableAllColumsFunctionArguments(tableObj)
				else:
					arguments = functionDetails[2]
				logging.info("Arguments %s", arguments)
				#3: Build templated stuff sensibly
				#Process the actual functions
				val += self.classFunctionTemplateCPP(className, returnValue, functionName, arguments, implementation, templateDict)
		return val

	# 	Class CPP: functions : (scope, name, argument(s))
	def buildSchemaClassCPP(self, className):
		ret = str()
		ret += self.constructorListCPP(className, self.CONSTRUCTOR_ARGS)
		ret += self.destructorCPP(className)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className, self.SCHEMA_FUNCTION_TEMPLATES)
		return ret
