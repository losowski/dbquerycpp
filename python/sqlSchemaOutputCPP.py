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

	def buildContents(self):
		output = str()
		output += self.fmt_ifndefine(self.schemaName())
		output += self.fmt_define(self.schemaName())
		#Incldues
		output += self.fmt_include(self.schemaName() + ".hpp")
		#Using Namespaces
		output += self.useNamespace("std")
		#output += self.useNamespace("dbquery") -- Unused
		#Code
		namespaced = str()
		#Build Class Functions
		namespaced += self.buildSchemaClassCPP(self.schemaName(), self.CONSTRUCTOR_ARGS, self.CONSTRUCTOR_INIT_CPP, self.SCHEMA_FUNCTION_TEMPLATES)
		#Make a namespace
		output += self.defineNamespace(self.schemaName(), namespaced)
		output += self.fmt_endifdefine(self.schemaName())
		return output
