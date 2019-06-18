#Schema Table

#import
import logging
import sqlSchemaTableBase
import sqlSchemaTableOutputHPP
import sqlSchemaTableOutputCPP
import sqlSchemaOutputSQL

class SQLSchemaTableOutput (sqlSchemaTableBase.SQLSchemaTableBase):

	def __init__(self, tableName):
		sqlSchemaTableBase.SQLSchemaTableBase.__init__(self, tableName)
		self.hpp =  sqlSchemaTableOutputHPP.SQLSchemaTableOutputHPP(self)
		self.cpp =  sqlSchemaTableOutputCPP.SQLSchemaTableOutputCPP(self)
		self.sql =  sqlSchemaOutputSQL.sqlSchemaOutputSQL(self)

	def __del__(self):
		sqlSchemaTableBase.SQLSchemaTableBase.__del__(self)
		self.hpp = None
		self.cpp = None
		self.sql = None


	def initialiseDataStructuresTable(self):
		self.hpp.initialiseDataStructuresTable()
		self.cpp.initialiseDataStructuresTable()
		#self.sql.initialiseDataStructures() #Unused as uses a different base class


	def build(self):
		self.hpp.build()
		self.cpp.build()
		self.sql.build()
