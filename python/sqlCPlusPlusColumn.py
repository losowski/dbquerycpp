#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusCommon

class SQLCPlusPlusTable (sqlCPlusPlusCommon.SQLCPlusPlusCommon):
	def __init__(self, outputObject, filename):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__init__(self, outputObject, filename)
		self.dataDict = None


	def __del__(self):
		sqlCPlusPlusCommon.SQLCPlusPlusCommon.__del__(self)
