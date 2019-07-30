#Schema Specific base functions

#import
import logging

class SQLSchema:
	def __init__(self, schemaName = "public"):
		self.schemaNameSQL = self.__generateSchemaNameSQL(schemaName)
		self.schemaNameCPP = self.__generateSchemaNameCPP(schemaName)

	def __del__(self):
		pass

	def __generateSchemaNameSQL(self, tableName):
		schemaName = tableName.split(".")[0]
		return schemaName

	def __generateSchemaNameCPP(self, tableName):
		schema = self.__generateSchemaNameSQL(tableName)
		schemaName = schema.split("_")[0]
		schemaName += ''.join( word.title() for word in schema.split("_")[1:])
		return schemaName

	def getSchemaNameCPP(self):
		return self.schemaNameCPP

	def getSchemaNameSQL(self):
		return self.schemaNameSQL

	def setSchema(self, schemaName):
		self.schemaNameSQL = self.__generateSchemaNameSQL(schemaName)
		self.schemaNameCPP = self.__generateSchemaNameCPP(schemaName)

