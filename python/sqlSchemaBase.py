#SQL Create DB File Parser

#import
import logging
import sqlSchemaTable

class SQLSchemaBase:
	def __init__(self, fileName):
		self.fileName = fileName
		self.tables	=	list()
		pass

	def __del__(self):
		pass

	def initialise(self):
		pass

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def shutdown(self):
		pass
