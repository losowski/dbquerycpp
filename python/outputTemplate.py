#!/usr/bin/python
#Generic Template handling

#import
import logging
from string import Template

class OutputTemplate:
	def __init__(self, templateFile, outputFile):
		self.templateFileName = templateFile
		self.outputFile = outputFile
		#Template contents
		self.templateFileContents = str()

	def __del__(self):
		pass

	def loadTemplate(self):
		print ("Loading template {templateFileName}".format(templateFileName = self.templateFileName))
		templateFileObject = open("templates/" + self.templateFileName, 'r')
		contents = templateFileObject.read()
		self.templateFileContents = Template(contents)
		templateFileObject.close()

	def generateSourceCode(self, dataMap):
		print ("Generating source code file {outputfile}".format(outputfile = self.outputFile))
		output = self.templateFileContents.safe_substitute(dataMap)
		outputFile = open(self.outputFile, 'w')
		outputFile.write(output)
		outputFile.flush()
		outputFile.close()
