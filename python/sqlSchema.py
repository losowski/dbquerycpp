#Schema Specific base functions

#import
import logging

class SQLSchema:
	def __init__(self, schemaName = "public"):
		self.schemaName = self.__generateSchemaName (schemaName)

	def __del__(self):
		pass

	def __generateSchemaName(self, tableName):
		schema = tableName.split(".")[0]
		schemaName = schema.split("_")[0]
		schemaName += ''.join( word.title() for word in schema.split("_")[1:])
		return schemaName

	def getSchemaName(self):
		return self.schemaName

	def setSchema(self, schema):
		self.schemaName = self.__generateSchemaName(schema)

