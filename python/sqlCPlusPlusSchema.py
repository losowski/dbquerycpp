#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusSchema (sqlCPlusPlusBase.SQLCPlusPlusBase):
	CONST_TABLENAME = 'tableName'
	CONST_TABLEVARS	= 'TABLEVARS'
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
																			(CONST_TABLEVARS, ""),
																		),
	"""//Get objects to return
	paptBody objects;
	//Get new transaction
	shared_ptr<pqxx::work> txn = transaction.newTransaction();
	//Build the SQL statement
	string sql = tBody::SQL_SELECT + " name = " + txn->quote(name) + ";";
	// Run the query
	pqxx::result res = txn->exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{{
		//Local variables for the data
		int id = 0;
		string name;
		//Set the data
		dbquery::DBSafeUtils::safeToInt(&id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&name, res[i]["name"]);
		//Build the actual object
		ptBody ptr_tbody = gtBody( id, name);
		//Store in returned list
		objects->push_back(ptr_tbody);

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

	# Header
	# Table Column Expander
	def getTableColumsFunctionHPP(self, tableObject):
		#TODO: implement this to return the list of table objects as a list
		ret = list()
		for columnName, columnObject in tableObject.getColumns().iteritems():
			ret.append(columnObject.getType(), columnObject.getName())
		return ret


	#	Templated Table Functions
	def templatedNamedFunctionHPP (self, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], templateDict = {self.CONST_TABLENAME : tableName,})
		return val



	#templateFunctions = (ret, functionNametemplate, arguments)
	#TODO: Make this function more generic (currently we assume all API functions are public, and this not an exhaustive list)
	def templatedTableFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		for tableName, tableObj in self.outputObject.tables.iteritems():
			val += self.templatedNamedFunctionHPP(tableObj.getName(), templateFunctions)
		return val

	# Templated function List
	def templatedTableFunctionListHPP_2(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		#1: Iterate over functions
		for functionDetails in templateFunctions:
			ret = functionDetails[0]
			functionName = functionDetails[1]
			#2: Iterate over tables
			for tableName, tableObj in self.outputObject.tables.iteritems():
				# Handle special arguments (first parameter is the CONST_TABLEVARS)
				if (self.CONST_TABLEVARS == functionDetails[2][0]):
					#Expand the arguments to the table parameters
					arguments = self.getTableColumsFunctionHPP()
				else:
					arguments = functionDetails[2]
				#Process the actual functions
				#TODO write the output
		#3: Build templated stuff sensibly
		return val


	# Storage objects to implement object caching
	#TODO: Implement means to generate storage objects
	#TODO: Add functions to retrieve via the stored object (and not just generate new objects) - header and implementation



	# Implementation
	#	Templated Table Functions
	def templatedNamedFunctionCPP (self, className, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = {self.CONST_TABLENAME : tableName,})
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListCPP(self, className):
		val = str()
		for tableObj in self.outputObject.tables.values():
			val += "//{tableName}\n".format(tableName = tableObj.getName())
			val += self.templatedNamedFunctionCPP(className, tableObj.getName(), self.SCHEMA_FUNCTION_TEMPLATES)
		return val

	# 	Class HPP: functions : (scope, name, argument(s))
	def buildSchemaClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		# Make functions
		ret += self.templatedTableFunctionListHPP(self.SCHEMA_FUNCTION_TEMPLATES)
		#TODO: Add function generator for new rows (not primary key driven)
		# Add Scoped variables
		ret += self.classScopeVariableHPP()
		ret += "};\n"
		return ret

	# 	Class CPP: functions : (scope, name, argument(s))
	def buildSchemaClassCPP(self, className):
		ret = str()
		ret += self.constructorListCPP(className, self.CONSTRUCTOR_ARGS)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className)
		return ret
