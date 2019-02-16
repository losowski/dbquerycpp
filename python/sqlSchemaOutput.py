#SQL Create DB File Parser

#import
import logging
import sqlSchemaBase
import sqlCPlusPlusBase

class SQLSchemaOutput (sqlSchemaBase.SQLSchemaBase, sqlCPlusPlusBase.SQLCPlusPlusBase):
	def __init__(self, fileName):
		sqlSchemaBase.SQLSchemaBase.__init__(self, fileName)
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self)
		pass

	def __del__(self):
		sqlSchemaBase.SQLSchemaBase.__del__(self)
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		pass
