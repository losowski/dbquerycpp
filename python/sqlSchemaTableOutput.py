#Schema Table

#import
import logging
import sqlSchemaTableBase

class SQLSchemaTableOutput (sqlSchemaTableBase.SQLSchemaTableBase):
	def __init__(self, tableName):
		sqlSchemaTableBase.SQLSchemaTableBase.__init__(self, tableName)

	def __del__(self):
		sqlSchemaTableBase.SQLSchemaTableBase.__del__(self) 
