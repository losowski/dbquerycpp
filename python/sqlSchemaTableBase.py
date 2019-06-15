#Schema Table

#import
import logging
import sqlSchema
import sqlSchemaTableColumn

class SQLSchemaTableBase (sqlSchema.SQLSchema):

	def __init__(self, tableName):
		sqlSchema.SQLSchema.__init__(self, tableName.split(".")[0])
		self.tableName = tableName.split(".")[1]
		self.tableFullName = tableName
		self.columns = dict()
		self.primaryKey = ""
		logging.info("Created table: %s", self.tableName)
		pass

	def __del__(self):
		sqlSchema.SQLSchema.__del__(self)
		pass

	def getFullName(self):
		return self.tableFullName

	def getName(self):
		return self.tableName

	def getColumns (self):
		return self.columns

	def getNonPrimaryKeyColums(self):
		output = dict()
		for columnName, columnObject in self.columns.iteritems():
			if (columnName != self.primaryKey):
				output[columnName] = columnObject
		return output

	def getNonPKColumnList(self):
		return ", ".join("{column}".format(column = columnName) for columnName, columnObject in self.getNonPrimaryKeyColums().iteritems())

	def getNonPKColumnTypeList(self):
		return ", ".join("{colType} {column}".format(column = columnName, colType = columnObject.getType() ) for columnName, columnObject in self.getNonPrimaryKeyColums().iteritems())

	#Primary Key
	# NOTE: Only support single column primary key (i.e the first index)
	def setPrimaryKey(self, primaryKey):
		self.primaryKey = primaryKey
		self.columns[primaryKey].setPrimaryKey(True)

	def getPrimaryKey (self):
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
