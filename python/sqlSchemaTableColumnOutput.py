#Schema Table

#import
import logging
import sqlSchemaTableColumnBase

class SQLSchemaTableColumnOutput (sqlSchemaTableColumnBase.SQLSchemaTableColumnBase):
	def __init__(self, columnName, columnType):
		sqlSchemaTableColumnBase.SQLSchemaTableColumnBase.__init__(self, columnName, columnType)

	def __del__(self):
		sqlSchemaTableColumnBase.SQLSchemaTableColumnBase.__del__(self)
