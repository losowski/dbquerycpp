#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusSchema (sqlCPlusPlusBase.SQLCPlusPlusBase):
	def __init__(self, outputObject, filename):
		completeFilename = outputObject.schema + filename
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, completeFilename)
		self.outputObject = outputObject


	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def tableName(self):
		return self.outputObject.tableName

	def schemaName(self):
		return self.outputObject.schemaName

	def buildContents(self):
		return str()


