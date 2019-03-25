#Schema Table

#import
import logging
import sqlSchemaTableColumnOutput

class SQLSchemaTableColumn (sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput):

	#Type converter
	SQLTYPEMAPPING	=	{
							'bigint'	:	'Int',
							'timestamp'	:	'String',
						}

	def __init__(self, columnName, columnType):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__init__(self, columnName, columnType)
		pass

	def __del__(self):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__del__(self)


	def getCPPType(self):
		return self.SQLTYPEMAPPING.get(self.columnType, 'String')
