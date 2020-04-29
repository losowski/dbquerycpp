#SQL Create DB File Parser

#import
import logging
import sqlSchema
import sqlSchemaOutputHPP
import sqlSchemaOutputCPP
import sqlSchemaOutputMakefile


class SQLSchemaBase (sqlSchema.SQLSchema):
	def __init__(self):
		sqlSchema.SQLSchema.__init__(self)
		self.logger = logging.getLogger('SQLSchemaBase')
		self.tables = dict()	#	tableName - TableObj
		self.hpp = None
		self.cpp = None
		self.makefile = None

	def __del__(self):
		sqlSchema.SQLSchema.__del__(self)
		self.hpp = None
		self.cpp = None
		self.makefile = None

	def loadData(self):
		# Called from the reader to build the data
		pass

	def getTables(self):
		return self.tables

	def initialise(self):
		# Build Makefile
		self.makefile = sqlSchemaOutputMakefile.SQLSchemaOutputMakefile(self)
		# Build the schema
		self.hpp = sqlSchemaOutputHPP.SQLSchemaOutputHPP(self)
		self.cpp = sqlSchemaOutputCPP.SQLSchemaOutputCPP(self)
		pass

	def initialiseDataStructures(self):
		#Builds the internal data structures
		#Initialise Schema files
		self.hpp.initialiseDataStructures()
		self.cpp.initialiseDataStructures()
		#Build Table files
		for tableName, tableObj in self.tables.iteritems():
			tableObj.initialiseDataStructuresTable()

	def build(self):
		#Build Makefile - buildContents not build (template, not a complete file builder)
		self.makefile.buildContents()
		#Build Schema files
		self.cpp.build()
		self.hpp.build()
		#Build Table files
		for tableName, tableObj in self.tables.iteritems():
			tableObj.build()

	def shutdown(self):
		pass
