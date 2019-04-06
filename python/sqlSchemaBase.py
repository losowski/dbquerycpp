#SQL Create DB File Parser

#import
import logging
import sqlSchemaOutputHPP
import sqlSchemaOutputCPP
import sqlSchemaOutputMakefile


class SQLSchemaBase:
	def __init__(self):
		self.tables = dict()	#	tableName - TableObj
		self.schema = "schema"
		self.hpp = None
		self.cpp = None
		self.makefile = None

	def __del__(self):
		self.hpp = None
		self.cpp = None
		self.makefile = None

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
		#Build Makefile - buildContents not build (template, not a complete file builder)
		self.makefile.buildContents()
		#Build Schema files
		self.cpp.build()
		self.hpp.build()
		#Build Table files
		for tableName, tableObj in self.tables.iteritems():
			tableObj.build()
			pass

	def run(self):
		# Build Makefile
		self.makefile = sqlSchemaOutputMakefile.SQLSchemaOutputMakefile(self)
		# Build the schema
		self.hpp = sqlSchemaOutputHPP.SQLSchemaOutputHPP(self)
		self.cpp = sqlSchemaOutputCPP.SQLSchemaOutputCPP(self)

	def shutdown(self):
		pass
