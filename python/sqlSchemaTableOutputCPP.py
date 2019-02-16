#File to implement the CPP file

#import
import logging
import sqlSchemaTableBase

class SQLSchemaTableOutputCPP:
	def __init__(self, outputObject):
		self.outputObject = outputObject

	def __del__(self):
		self.outputObject = None
