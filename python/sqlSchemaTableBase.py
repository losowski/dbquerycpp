#Schema Table

#import
import logging
import sqlSchemaTableColumn

class SQLSchemaTableBase:

	def __init__(self, tableName):
		self.schemaName = self.__buildSchemaName(tableName)
		self.tableName = tableName.split(".")[1]
		self.tableFullName = tableName
		self.columns = dict()
		self.primaryKey = ""
		logging.info("Created table: %s", self.tableName)
		pass

	def __del__(self):
		pass

	def __buildSchemaName(self, tableName):
		schema = tableName.split(".")[0]
		schemaName = schema.split("_")[0]
		schemaName += ''.join( word.title() for word in schema.split("_")[1:])
		return schemaName

	def getFullName(self):
		return self.tableFullName

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
