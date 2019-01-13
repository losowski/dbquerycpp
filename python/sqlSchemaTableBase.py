#Schema Table

#import
import logging

class SQLSchemaTableBase:

	def __init__(self, tableName):
		self.tableName = tableName
		self.primaryKey	=	""
		self.fields = dict()	#Field : (Table, ForeignKey)/None
		logging.debug("Created table: %s", self.tableName)
		pass

	def __del__(self):
		pass

	def getName (self):
		return self.tableName

	#Primary Key
	def setPrimaryKey (self, primaryKey):
		self.primaryKey = primaryKey

	def getPrimaryKey (self, primaryKey):
		return self.primaryKey
