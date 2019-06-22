#Schema Table

#import
import logging
import sqlSchemaTableColumnOutput

class SQLSchemaTableColumn (sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput):

	#Type converter
	SQLSAFETYPEMAPPING	=	{
							'bigint'	:	'Int',
							'char'		:	'String',
							'text'		:	'String',
							'timestamp'	:	'String',
						}

	def __init__(self, columnName, columnType):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__init__(self, columnName, columnType)
		pass

	def __del__(self):
		sqlSchemaTableColumnOutput.SQLSchemaTableColumnOutput.__del__(self)


	def getCPPSafeType(self):
		return self.SQLSAFETYPEMAPPING.get(self.columnType, 'String')

	def getCPPReferenceType(self):
		return self.SQLSAFETYPEMAPPING.get(self.columnType, 'String').lower()
