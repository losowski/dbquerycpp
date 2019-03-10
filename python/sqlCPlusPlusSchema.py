#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusSchema (sqlCPlusPlusBase.SQLCPlusPlusBase):
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							(
								("const string &", "connection",),
							),	#One constructor
						)

	#Schema templates - (ret, functionNametemplate, arguments)
	SCHEMA_FUNCTION_TEMPLATES =	(
									("p{tableName}", "g{tableName}", (
																			("int", "primaryKey"),
																		)
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

	#Templated Table Functions
	def templatedNamedFunctionHPP (self, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], templateDict = {self.CONST_TABLENAME : tableName,})
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n\t\t//Get single child objects\n"
		for tableName, tableObj in self.outputObject.tables.iteritems():
			val += "\t\t" + self.templatedNamedFunctionHPP(tableObj.getName(), templateFunctions) + ";\n"
		return val


	# 	Class HPP: functions : (scope, name, argument(s)) 
	def buildSchemaClassHPP(self, className, derivedClass, constructors, functions):
		ret = self.classNameDefinition(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, constructors)
		#TODO: Make functions
		ret += self.templatedTableFunctionListHPP(functions)
		ret += "}\n"
		return ret
