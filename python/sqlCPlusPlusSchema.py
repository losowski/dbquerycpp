#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusSchema (sqlCPlusPlusBase.SQLCPlusPlusBase):
	CONST_TABLENAME = 'tableName'
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							#One constructor
							(
								("const string &", "connection",),
							),
						)


	CONSTRUCTOR_INIT_CPP =	(	#One constructor
								(
									("dbquery::DBConnection", ("connection",),),
								)
							),

	SCHEMA_FUNCTION_TEMPLATES =	(
									("p{tableName}", "g{tableName}", (
																			("int", "primaryKey"),
																		),
	"""	shared_ptr<{tableName}> obj(new {tableName}(this, primaryKey) );
	obj->selectRow();
	return obj;""",
									),
								)






	def __init__(self, outputObject, extension):
		filename = outputObject.getSchema() + extension
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.outputObject = outputObject


	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def schemaName(self):
		return self.outputObject.getSchema().capitalize()

	def buildContents(self):
		return str()

	#Get Table Includes
	def getTableIncludes(self):
		ret = str()
		for tableName, tableObj in self.outputObject.tables.iteritems():
			ret += self.fmt_include(tableObj.getName() + ".hpp")
		return ret

	# Header
	#	Templated Table Functions
	def templatedNamedFunctionHPP (self, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], templateDict = {self.CONST_TABLENAME : tableName,})
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		for tableName, tableObj in self.outputObject.tables.iteritems():
			val += "\t\t" + self.templatedNamedFunctionHPP(tableObj.getName(), templateFunctions) + ";\n"
		return val

	# Implementation
	#	Templated Table Functions
	def templatedNamedFunctionCPP (self, className, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = {self.CONST_TABLENAME : tableName,})
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListCPP(self, className, templateFunctions):
		val = "//Functions to get single child objects\n"
		for idx, tableObj in enumerate(self.outputObject.tables.values()):
			val += "//{tableName}\n".format(tableName = tableObj.getName())
			val += self.templatedNamedFunctionCPP(className, tableObj.getName(), templateFunctions)
		return val

	# 	Class HPP: functions : (scope, name, argument(s))
	def buildSchemaClassHPP(self, className, derivedClass, constructors, functions):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, constructors)
		# Make functions
		ret += self.templatedTableFunctionListHPP(functions)
		ret += "}\n"
		return ret

	# 	Class CPP: functions : (scope, name, argument(s))
	def buildSchemaClassCPP(self, className, constructors, constructionArgs, functions):
		ret = str()
		ret += self.constructorListCPP(className, constructors, constructionArgs)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className, functions)
		return ret
