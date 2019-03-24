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
		ret += "}\n"
		return ret

	# 	Class CPP: functions : (scope, name, argument(s))
	def buildSchemaClassCPP(self, className):
		ret = str()
		ret += self.constructorListCPP(className, self.CONSTRUCTOR_ARGS)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className)
		return ret
