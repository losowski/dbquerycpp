#File to implement the HPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusTable

class SQLSchemaTableOutputHPP (sqlCPlusPlusTable.SQLCPlusPlusTable):
	def __init__(self, outputObject):
		sqlCPlusPlusTable.SQLCPlusPlusTable.__init__(self, outputObject, outputObject.tableName+".hpp")


	def __del__(self):
		sqlCPlusPlusTable.SQLCPlusPlusTable.__del__(self)

	def buildContents(self):
		output = str()
		output += self.fmt_ifndefine(self.tableFullName())
		output += self.fmt_define(self.tableFullName())
		output += self.fmt_include("dbresult.hpp")
		output += self.fmt_include("dbsafeutils.hpp")
		output += self.useNamespace("std")
		output += self.useNamespace("dbquery")
		namespaced = str()
		#Class Forward Definition
		namespaced += self.className(self.tableName())
		#TODO: Add typedefs
		#Build Class Functions
		namespaced += self.buildClassHPP(self.tableName(), "dbquery::DBResult")
		output += self.defineNamespace(self.schemaName(), namespaced)

		output += self.fmt_endifdefine(self.tableFullName())
		return output
