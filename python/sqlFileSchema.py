#SQL Create DB File Parser

#import
import logging
#import sqlTables

class SQLFileSchema:
	def __init__(self, fileName):
		self.fileName = fileName
		self.tables	=	list()
		pass

	def __del__(self):
		pass

	def initialise(self):
		# Open file
		# Read in contents
		pass

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def shutdown(self):
		pass
