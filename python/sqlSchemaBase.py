#SQL Create DB File Parser

#import
import logging

class SQLSchemaBase:
	def __init__(self):
		self.tables = dict()	#	tableName - TableObj
		self.schema = "demo" #TODO: Implement this properly
		pass

	def __del__(self):
		pass

	def initialise(self):
		pass

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def getSchema(self):
		return self.schema

	def shutdown(self):
		pass
