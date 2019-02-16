#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusTable (sqlCPlusPlusBase.SQLCPlusPlusBase):
	def __init__(self, outputObject, filename):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self)
		self.outputObject = outputObject
		self.fileName = filename

	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None


	def buildContents(self):
		return str()

	def build(self):
		outputFile = open(self.fileName, 'w')
		#Build the output contents
		output = self.buildContents()
		#Write the File
		outputFile.write(output)
		outputFile.flush()
		outputFile.close()
