#SQL Create DB File Parser

#import
import logging
import sqlSchemaBase

class SQLSchemaFile (sqlSchemaBase.SQLSchemaBase):
	def __init__(self, fileName):
		sqlSchemaBase.SQLSchemaBase.__init__(self, fileName)
		self.schemaFile = None
		pass

	def __del__(self):
		sqlSchemaBase.SQLSchemaBase.__del__(self)
		pass

	def initialise(self):
		# Open file
		self.schemaFile = open(self.fileName, 'r')
		# Read in contents
		fileContents = self.schemaFile.readlines()
		for line in fileContents:
			logging.debug("Line %s", line)
		# Close file
		self.schemaFile.close()

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def shutdown(self):
		pass
