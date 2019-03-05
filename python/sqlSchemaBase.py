#SQL Create DB File Parser

#import
import logging

class SQLSchemaBase:
	def __init__(self):
		self.tables = dict()	#	tableName - TableObj
		self.schema = "schema"
		self.hpp = None
		self.cpp = None

	def __del__(self):
		self.hpp = None
		self.cpp = None

	def initialise(self):
		pass

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def setSchema(self, schema):
		self.schema = schema

	def getSchema(self):
		return self.schema

	def build(self):
		#Build Schema files
		self.cpp.build()
		self.hpp.build()
		#Build Table files
		for tableName, tableObj in self.tables.iteritems():
			tableObj.build()
			pass

	def shutdown(self):
		pass
