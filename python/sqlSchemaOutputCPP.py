#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusSchema

class SQLSchemaOutputCPP (sqlCPlusPlusSchema.SQLCPlusPlusSchema):
	def __init__(self, outputObject):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__init__(self, outputObject, ".cpp")

	def __del__(self):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__del__(self)

	def schemaInitialiseDataStructures(self):
		pass


	def tableInitialiseDataStructures(self, tableName, tableObj):
		pass


	def buildContents(self):
		output = str()
		#Incldues
		output += self.fmt_include(self.schemaName() + ".hpp")
		#Using Namespaces
		output += self.useNamespace("std")
		#output += self.useNamespace("dbquery") -- Unused
		#Code
		namespaced = str()
		#Build Class Functions
		namespaced += self.buildSchemaClassCPP(self.schemaName())
		#Make a namespace
		output += self.defineNamespace(self.schemaName(), namespaced)
		return output
