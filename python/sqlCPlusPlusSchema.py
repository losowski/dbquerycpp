#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusSchema (sqlCPlusPlusBase.SQLCPlusPlusBase):
	#Dictionary helper definition
	CONST_TABLENAME 		= 'tableName'
	#Special codes for use in functions to use a table generator function
	CONST_INSERTCOLUMNS		= 'CONST_INSERTCOLUMNS'
	CONST_NONPKTABLEVARS	= 'NONPKTABLEVARS'
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
	#	1	-	Primary Key lookup (DONE - primaryKey)
	#	2	-	Insertion function (uses all elements that are not PK) (DONE - CONST_INSERTCOLUMNS)
	#	3	-	Generic WHERE lookup function (data agnostic)
	#	4	-	For each foreign Key -
	#				Lookup function by key
	SCHEMA_FUNCTION_TEMPLATES =	(
									("p{tableName}", "g{tableName}", (
																			("int", "primaryKey"),
																		),
	"""//Attempt to find the object
	map{tableName}::iterator it = {tableName}Map.find(primaryKey);
	p{tableName} ptr_{tableName};
	// If cannot be found in cache, create a new object
	if (it == {tableName}Map.end())
	{{
		p{tableName} obj(new {tableName}(this, primaryKey) );
		//Check data exists
		if (obj->selectRow() == true)
		{{
			obj->selectRow();
			//Store Object by Primary key
			{tableName}Map[obj->pk] = obj;
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
									("p{tableName}", "g{tableName}", (
																			(CONST_INSERTCOLUMNS, ""), #TODO: Run selects inline
																		),
	"""	p{tableName} obj(new {tableName}(this, {NonPKColumns}) );
	//Store Object by Primary key
	{tableName}Map[obj->id] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	transaction.addInsertElement(obj);
	//Return object
	return obj;""",
									),
									("p{tableName}", "g{tableName}", (
																			("string", "sqlWhereClause"),
																		),
	"""//Get objects to return
	pap{tableName} objects;
	//Get new transaction
	shared_ptr<pqxx::work> txn = transaction.newTransaction();
	//Build the SQL statement
	string sql = {tableName}::SQL_SELECT << sqlWhereClause << ";";
	// Run the query
	pqxx::result res = txn->exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
		//Local variables for the data
		{DBSafeUtilsColumnVariables}
		//Set the data
		{DBSafeUtilsColumns}
		//Build the actual object
		p{tableName} ptr_{tableName} = g{tableName}( id, name);
		//Store in returned list
		objects->push_back(ptr_{tableName});

	}}
	//Return objects
	return objects;""",
									),
								)

	def __init__(self, outputObject, extension):
		filename = outputObject.getSchemaName() + extension
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.outputObject = outputObject


	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

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
	def getTableColumsFunctionArguments(self, tableObject):
		#TODO: implement this to return the list of table objects as a list
		ret = list()
		for columnName, columnObject in tableObject.getNonPrimaryKeyColums().iteritems():
			logging.debug("getTableColumsFunctionArguments columnName %s", columnName)
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
					arguments = self.getTableColumsFunctionArguments(tableObj)
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
		ret += self.destructorListHPP(className)
		# Make functions
		ret += self.templatedTableFunctionListHPP(self.SCHEMA_FUNCTION_TEMPLATES)
		#TODO: Add function generator for new rows (not primary key driven)
		# Add Scoped variables
		ret += self.classScopeVariableHPP()
		ret += "};\n"
		return ret

	# ---- Implementation ----
	# Templated CPP function List
	#TODO: Implement column conversions for "dbquery::DBSafeUtils::safeToInt(&id, res[i]["id"]);"
	#TODO: Implement usage of the table specific select statement (requires constant string)
	def templatedTableFunctionListCPP(self, className, templateFunctions):
		val = str()
		#1: Iterate over tables
		for tableName, tableObj in self.outputObject.tables.iteritems():
			templateDict =	{
								self.CONST_TABLENAME			:	tableObj.getName(),
								"NonPKColumns" 					:	tableObj.getNonPKColumnList(),
								"DBSafeUtilsColumns" 			:	"//TODO: DBSafeUtilsColumns",
								"DBSafeUtilsColumnVariables" 	:	"//TODO: DBSafeUtilsColumnVariables",
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
					arguments = self.getTableColumsFunctionArguments(tableObj)
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
