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
		#TODO: Implement this function
		return output
