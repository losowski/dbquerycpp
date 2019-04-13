#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusTable

class SQLSchemaTableOutputCPP (sqlCPlusPlusTable.SQLCPlusPlusTable):
	def __init__(self, outputObject):
		sqlCPlusPlusTable.SQLCPlusPlusTable.__init__(self, outputObject, outputObject.tableName+".cpp")

	def __del__(self):
		sqlCPlusPlusTable.SQLCPlusPlusTable.__del__(self)

	def buildContents(self):
		output = str()
		#Incldues
		output += self.fmt_include("dbsafeutils.hpp")
		output += self.fmt_include(self.tableName() + ".hpp")
		#Using Namespaces
		output += self.useNamespace("std")
		output += self.useNamespace("dbquery")
		#Code
		namespaced = str()
		#Build Class Functions
		namespaced += self.buildTableClassCPP(self.tableName())
		#Make a namespace
		output += self.defineNamespace(self.schemaName(), namespaced)
		return output
