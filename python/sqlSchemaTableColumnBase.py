#Schema Table

#import
import logging

class SQLSchemaTableColumnBase:

	def __init__(self, columnName, columnType):
		self.columnName = columnName
		self.columnType = columnType
		self.sequenceName = None
		self.primaryKey	=	False
		self.referencedTable = None
		self.referencedColumn = None
		logging.info("Created Column: %s  (%s)", self.columnName, self.columnType)

	def __del__(self):
		pass

	def getName(self):
		return self.columnName

	def getType(self):
		return self.columnType

	#Sequence
	def setSequence(self, sequence):
		self.sequenceName = sequence

	def getSequence(self):
		return self.sequenceName

	#Primary Key
	def setPrimaryKey(self, primaryKey):
		self.primaryKey = primaryKey

	def isPrimaryKey(self):
		return self.primaryKey

	#Foreign Key Links
	def addForeignKey (self, referencedTable, referencedColumn):
		self.referencedTable = referencedTable
		self.referencedColumn = referencedColumn

	def getForeignKeyTable(self):
		return self.referencedTable

	def getForeignKeyColumn(self):
		return self.referencedColumn

