#Schema Table

#import
import logging
import collections

import sqlSchema
import sqlSchemaTableColumn

class SQLSchemaTableBase (sqlSchema.SQLSchema):

	def __init__(self, tableName):
		sqlSchema.SQLSchema.__init__(self, tableName.split(".")[0])
		self.logger = logging.getLogger('SQLSchemaTableBase')
		self.tableName		= tableName.split(".")[1]
		self.tableFullName	= tableName
		self.columns		= dict()
		self.primaryKey		= ""
		self.sequenceList	= dict()
		self.logger.debug("Created table: %s", self.tableName)
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
		output = collections.OrderedDict()
		for columnName, columnObject in self.columns.iteritems():
			if (columnName != self.primaryKey):
				output[columnName] = columnObject
		return output

	# Primary Key Only functions
	def getNonPKColumnList(self):
		return ", ".join("{column}".format(column = columnName) for columnName, columnObject in self.getNonPrimaryKeyColums().iteritems())

	def getNonPKColumnTypeList(self):
		return ", ".join("{colType} {column}".format(column = columnName, colType = columnObject.getType() ) for columnName, columnObject in self.getNonPrimaryKeyColums().iteritems())

	# All colums
	def getAllColumnList(self):
		return ", ".join("{column}".format(column = columnName) for columnName, columnObject in self.getColumns().iteritems())

	def getAllColumnTypeList(self):
		return ", ".join("{colType} {column}".format(column = columnName, colType = columnObject.getType() ) for columnName, columnObject in self.getColumns().iteritems())

	#Primary Key
	# NOTE: Only support single column primary key (i.e the first index)
	def setPrimaryKey(self, primaryKey):
		self.primaryKey = primaryKey
		self.primaryKeyType = self.columns[primaryKey].getCPPReferenceType()
		self.columns[primaryKey].setPrimaryKey(True)

	def getPrimaryKey (self):
		return self.primaryKey

	def getPrimaryKeyType (self):
		return self.primaryKeyType

	#Column and type
	def addColumn(self, columnName, columnType):
		self.logger.debug("Adding column: \"%s\" - \"%s\"", columnName, columnType)
		#Build column object
		columnObj = sqlSchemaTableColumn.SQLSchemaTableColumn (columnName, columnType)
		#Add the column object
		self.columns[columnName] = columnObj
		return columnObj

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

	#Sequence
	def getSequencePrimaryKey(self):
		output = None
		for columnName, columnObject in self.columns.iteritems():
			if (True == columnObject.isPrimaryKey()):
				output = columnObject.getSequence()
				break
		return output


	def addSequences(self, sequenceDict):
		for sequence, sequenceSQL in sequenceDict.items():
			self.logger.debug("Adding sequence= %s", sequence)
			self.sequenceList[sequence] = sequenceSQL

	def getSequences(self):
		self.logger.debug("Current Sequence list = %s", self.sequenceList)
		return self.sequenceList
