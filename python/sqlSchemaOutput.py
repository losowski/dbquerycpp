#SQL Create DB File Parser

#import
import logging
import sqlSchemaBase

class SQLSchemaOutput (sqlSchemaBase.SQLSchemaBase):
	def __init__(self, fileName):
		sqlSchemaBase.SQLSchemaBase.__init__(self, fileName)
		pass

	def __del__(self):
		sqlSchemaBase.SQLSchemaBase.__del__(self)
		pass
