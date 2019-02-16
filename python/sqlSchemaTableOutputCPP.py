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
		#TODO: Implement this function
		return output
