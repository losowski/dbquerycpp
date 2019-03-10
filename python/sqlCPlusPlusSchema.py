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
	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedFunctionListHPP(self, templateFunctions):
		val = "\tpublic:\n"
		for tableName, tableObj in self.outputObject.tables.iteritems():
			val += "\t\t" + self.templatedNamedFunctionHPP(tableObj.getName(), templateFunctions) + ";\n\n"
		return val
