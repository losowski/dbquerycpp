#Schema Table

#import
import logging
import sqlSchemaTableOutput

class SQLSchemaTable (sqlSchemaTableOutput.SQLSchemaTableOutput):
	def __init__(self, tableName):
		sqlSchemaTableOutput.SQLSchemaTableOutput.__init__(self, tableName) 
		pass

	def __del__(self):
		sqlSchemaTableOutput.SQLSchemaTableOutput.__del__(self)
