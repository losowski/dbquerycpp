#SQL Create DB File Parser

#import
import logging
import sqlSchemaBase
import re

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
			reComment = re.search('^[A-Z].*', line)
			if (reComment != None):
				comment = reComment.group(0)
				logging.info("Match: %s", comment)
			else:
				logging.info("No Match: %s", reComment)
		# Close file
		self.schemaFile.close()

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def shutdown(self):
		pass
