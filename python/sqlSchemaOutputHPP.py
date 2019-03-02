#File to implement the HPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusSchema

class SQLSchemaOutputHPP (sqlCPlusPlusSchema.SQLCPlusPlusSchema):
	def __init__(self, outputObject):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__init__(self, outputObject, ".hpp")


	def __del__(self):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__del__(self)

	def buildContents(self):
		output = str()
		output += self.fmt_ifndefine(self.schemaName())
		output += self.fmt_define(self.schemaName())
		output += self.fmt_include("dbresult.hpp")
		output += self.useNamespace("std")
		output += self.useNamespace("dbquery")
		namespaced = str()
		output += self.defineNamespace(self.schemaName(), namespaced)
		output += self.fmt_include("dbsafeutils")
		output += self.fmt_endifdefine(self.schemaName())
		return output
