#Schema Table

#import
import logging
import sqlSchemaTableColumnOutput

class SQLSchemaTableColumn (sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput):
	def __init__(self, columnName, columnType):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__init__(self, columnName, columnType)
		pass

	def __del__(self):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__del__(self)
