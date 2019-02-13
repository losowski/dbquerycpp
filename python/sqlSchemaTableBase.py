#Schema Table

#import
import logging
import sqlSchemaTableColumn

class SQLSchemaTableBase:

	def __init__(self, tableName):
		self.tableName = tableName
		self.columns = dict()
		self.primaryKey = ""
		logging.info("Created table: %s", self.tableName)
		pass

	def __del__(self):
		pass

	def getName(self):
		return self.tableName

	#Primary Key
	# NOTE: Only support single column primary key (i.e the first index)
	def setPrimaryKey(self, primaryKey):
		self.primaryKey = primaryKey
		self.columns[primaryKey].setPrimaryKey(True)

	def getPrimaryKey (self, primaryKey):
		return self.primaryKey

	#Column and type
	def addColumn(self, columnName, columnType):
		logging.info("Adding column: \"%s\" - \"%s\"", columnName, columnType)
		self.columns[columnName] = sqlSchemaTableColumn.SQLSchemaTableColumn (columnName, columnType)

	#Foreign Key Links
	def addForeignKey(self, foreignKeyName, myColumn, referencedTable, referencedColumn):
		#TODO: Think how to implement this properly
		#self.foreignKeys[myColumn] = 
		pass

	#Index
	def addIndex(self, indexName, indexColumn):
		#TODO: This should create a function same as the foreign key
		#	Perhaps a set to avoid duplication of columns
		pass
