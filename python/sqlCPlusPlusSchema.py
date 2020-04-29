#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusCommon

class SQLCPlusPlusSchema (sqlCPlusPlusCommon.SQLCPlusPlusCommon):
	#Dictionary helper definition
	CONST_PRIMARY_KEY_TYPE	= 'primaryKeyType'
	CONST_TABLENAME 		= 'tableName'
	#Special codes for use in functions to use a table generator function
	CONST_INSERTCOLUMNS		= 'CONST_INSERTCOLUMNS'
	CONST_ALLCOLUMNS		= 'CONST_ALLCOLUMNS'
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							#One constructor
							(
								#Parameters
								(
									#DBConnection & connection, DBTransaction * transaction
									("DBConnection &", "connection",),
									("DBTransaction *", "transaction",),
								),
								#Args
								(
									("dbquery::DBSchemaBase", ("connection", "transaction"),),
								),
							),
						)

	#Schema function for initialising
	# Functions:
	#	1	-	returnValue
	#	2	-	functionName
	#	3	-	arguments (list: (type, name)
	#	4	-	const (included once at top of function)
	#	5	-	impl (templatd by class name)
	SCHEMA_BASIC_FUNCTION_TEMPLATE	=	(
									(None , "void", "initialise", (
																			("void", ""),
																		),
	None,
	"""\n\t{className}::initialise(mdbconnection);""",
									),
									(None , "void", "purgeCachedObjects", (
																			("void", ""),
																		),
	"""\n\t// Get Current time
	clock_t currentTime = clock() + CACHE_INTERVAL;
	// For each map, decide on caching""",
	"""\n\t// {className} Cache checking
	//Create list to clear
	list < int > {className}List;
	// Iterate over entries
	for (map{className}::iterator it = {className}Map.begin(); it != {className}Map.end(); it++)
	{{{{
		if (it->second->canPurgeCache(currentTime))
		{{{{
			//Add to list
			{className}List.push_back(it->first);
		}}}}
	}}}}
	// Clear through list to avoid destroying the map
	for (list < int >::iterator delit = {className}List.begin(); delit != {className}List.end(); delit++)
	{{{{
		{className}Map.erase(*delit);
	}}}}
""",
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
									(None , "p{tableName}", "get{tableName}", (
																			(CONST_ALLCOLUMNS, ""),
																		),
	"""	p{tableName} obj(new {tableName}(mdbconnection, {AllColumns}) );
	//Store Object by Primary key
	{tableName}Map[obj->get{PrimaryKeyAccessor}()] = obj;
	mtransaction->addUpdateElement(obj);
	//Return object
	return obj;""",
									),
									(None , "p{tableName}", "g{tableName}", (
																			("{primaryKeyType}", "primaryKey"),
																		),
	"""//Attempt to find the object
	map{tableName}::iterator it = {tableName}Map.find(primaryKey);
	p{tableName} ptr_{tableName};
	// If cannot be found in cache, create a new object
	if (it == {tableName}Map.end())
	{{
		p{tableName} obj(new {tableName}(mdbconnection, primaryKey) );
		//Check data exists
		bool exists = obj->selectRow();
		if (true == exists)
		{{
			//Store Object by Primary key
			{tableName}Map[obj->get{PrimaryKeyAccessor}()] = obj;
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
	//Update
	mtransaction->addUpdateElement(ptr_{tableName});
	return ptr_{tableName};""",
									),
									(None , "p{tableName}", "insert{tableName}", (
																			(CONST_INSERTCOLUMNS, ""), #TODO: Run selects inline
																		),
	"""	p{tableName} obj(new {tableName}(mdbconnection, {NonPKColumns}) );
	//Store Object by Primary key
	{tableName}Map[obj->get{PrimaryKeyAccessor}()] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	mtransaction->addInsertElement(obj);
	//Return object
	return obj;""",
									),
									(None , "pap{tableName}", "getMultiple{tableName}", (
																			("string &", "sqlWhereClause"),
																		),
	"""//Get objects to return
	pap{tableName} objects;
	//Get new transaction
	pqxx::work txn(*mdbconnection);
	//Build the SQL statement
	string sql = {tableName}::SQL_SELECT + sqlWhereClause + ";";
	// Run the query
	pqxx::result res = txn.exec(sql);
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
					(None , "void", "delete{tableName}", (
																			("{primaryKeyType}", "primaryKey"),
																		),
	"""//Retrieve the object
	map{tableName}::iterator it = {tableName}Map.find(primaryKey);
	//If found, remove from map
	if (it != {tableName}Map.end())
	{{
		//Add element to the delete queue
		mtransaction->addDeleteElement(it->second);
	}}
	// Else if not found - load for query
	else if (it == {tableName}Map.end())
	{{
		//Load object
		p{tableName} obj = g{tableName}(primaryKey);
		//Delete the object
		mtransaction->addDeleteElement(obj);
	}}
	//Remove element from the stored object list
	{tableName}Map.erase(primaryKey);""",
									),
								)

	def __init__(self, outputObject, extension):
		filename = outputObject.getSchemaNameCPP() + extension
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__init__(self, outputObject, filename)
		self.logger = logging.getLogger('SQLCPlusPlusSchema')


	def __del__(self):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__del__(self)


	def schemaName(self):
		return self.outputObject.getSchemaNameCPP()


	#Complex Data structure Builder
	def schemaInitialiseDataStructures(self):
		# Override this class
		self.logger.error("schemaInitialiseDataStructures not overridden")
		pass

	def tableInitialiseDataStructures(self, tableName, tableObj):
		#Table specific building
		# Override this class
		self.logger.error("tableInitialiseDataStructures not overridden")
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
			self.logger.debug("getTableNonPKColumsFunctionArguments columnName %s", columnName)
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
	#NOTE: This schema function works differently:
	#	Make function definition
	#	Content of function is interpreted as a template (specifically CPP version)
	def templatedFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\n"
		#define the template Dictionary
		templateDict = dict()
		#1: Iterate over Functions
		for functionDetails in templateFunctions:
			keyWord = functionDetails[0]
			returnValue = functionDetails[1]
			functionName = functionDetails[2]
			arguments = functionDetails[3]
			#Process the actual functions
			val += self.classFunctionTemplateHPP(keyWord, returnValue, functionName, arguments, templateDict)
		return val

	# Templated HPP function List
	def templatedTableFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		#1: Iterate over tables
		for tableName, tableObj in self.outputObject.tables.iteritems():
			templateDict =	{
					self.CONST_TABLENAME		:	tableObj.getName(),
					"NonPKColumns" 				:	tableObj.getNonPKColumnList(),
					self.CONST_PRIMARY_KEY_TYPE	:	tableObj.getPrimaryKeyType(),
				}
			#2: Iterate over functions
			for functionDetails in templateFunctions:
				keyWord = functionDetails[0]
				returnValue = functionDetails[1]
				functionName = functionDetails[2]
				args = (())
				# Handle special arguments (first parameter is the CONST_TABLEVARS)
				self.logger.debug("functionDetails Argument HPP %s", functionDetails[3][0][0])
				if (self.CONST_INSERTCOLUMNS == functionDetails[3][0][0]):
					#Expand the arguments to the table parameters to allow insert
					arguments = self.getTableNonPKColumsFunctionArguments(tableObj)
				elif (self.CONST_ALLCOLUMNS == functionDetails[3][0][0]):
					#Expand the arguments to the table parameters to all columns
					arguments = self.getTableAllColumsFunctionArguments(tableObj)
				else:
					arguments = functionDetails[3]
				self.logger.debug("Arguments %s", arguments)
				#3: Build templated stuff sensibly
				#Process the actual functions
				val += self.classFunctionTemplateHPP(keyWord, returnValue, functionName, arguments, templateDict)
		return val

	# 	Class HPP: functions : (scope, name, argument(s))
	def buildSchemaClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		ret += self.destructorHPP(className)
		# Make functions
		ret += self.templatedFunctionListHPP(self.SCHEMA_BASIC_FUNCTION_TEMPLATE)
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
			self.logger.debug("getSafeTypeVariables column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\t{datatype} {column};\n".format(column = columnName, datatype = columnData.getCPPReferenceType())
		return val

	# Templated CPP function List
	#NOTE: This schema function works differently:
	#	Make function definition
	#	Content of function is interpreted as a template (specifically CPP version)
	def templatedFunctionListCPP(self, className, templateFunctions):
		val = str()
		templateDict =	dict()
		#2: Iterate over functions
		for functionDetails in templateFunctions:
			#keyWord = functionDetails[0] # UNUSED
			returnValue = functionDetails[1]
			functionName = functionDetails[2]
			arguments = functionDetails[3]
			const = functionDetails[4]
			impl = functionDetails[5]
			# implementation string
			implementation = str()
			self.logger.debug("templatedFunctionListCPP const\"%s\"", const)
			if (None != const):
				implementation += const
			self.logger.debug("templatedFunctionListCPP impl\"%s\"", impl)
			for tableName, tableObj in self.outputObject.tables.iteritems():
				self.logger.debug("templatedFunctionListCPP className\"%s\"", tableObj.getName())
				implementation += impl.format(className = tableObj.getName())
			#Process the actual functions
			val += self.classFunctionTemplateCPP(className, returnValue, functionName, arguments, implementation, templateDict)
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
								"PrimaryKeyAccessor"			:	tableObj.getPrimaryKey().title(),
								self.CONST_PRIMARY_KEY_TYPE		:	tableObj.getPrimaryKeyType(),
							}
			#2: Iterate over functions
			for functionDetails in templateFunctions:
				#keyWord = functionDetails[0] # UNUSED
				returnValue = functionDetails[1]
				functionName = functionDetails[2]
				args = (())
				implementation = functionDetails[4]
				# Handle special arguments (first parameter is the CONST_TABLEVARS)
				self.logger.debug("functionDetails Argument CPP %s", functionDetails[3][0][0])
				if (self.CONST_INSERTCOLUMNS == functionDetails[3][0][0]):
					#Expand the arguments to the table parameters to allow insert
					arguments = self.getTableNonPKColumsFunctionArguments(tableObj)
				elif (self.CONST_ALLCOLUMNS == functionDetails[3][0][0]):
					#Expand the arguments to the table parameters to all columns
					arguments = self.getTableAllColumsFunctionArguments(tableObj)
				else:
					arguments = functionDetails[3]
				self.logger.debug("Arguments %s", arguments)
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
		ret += self.templatedFunctionListCPP(className, self.SCHEMA_BASIC_FUNCTION_TEMPLATE)
		ret += self.templatedTableFunctionListCPP(className, self.SCHEMA_FUNCTION_TEMPLATES)
		return ret
