#Schema Table

#import
import logging
import sqlSchemaTableBase
import sqlSchemaTableOutputHPP
import sqlSchemaTableOutputCPP

class SQLSchemaTableOutput (sqlSchemaTableBase.SQLSchemaTableBase):
	def __init__(self, tableName):
		sqlSchemaTableBase.SQLSchemaTableBase.__init__(self, tableName)
		self.hpp =  sqlSchemaTableOutputHPP.SQLSchemaTableOutputHPP(self)
		self.cpp =  sqlSchemaTableOutputCPP.SQLSchemaTableOutputCPP(self)

	def __del__(self):
		sqlSchemaTableBase.SQLSchemaTableBase.__del__(self)
		self.hpp = None
		self.cpp = None

	def build(self):
		self.hpp.build()
		self.cpp.build()
