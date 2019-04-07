#File to implement the CPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import outputTemplate

class SQLSchemaOutputMakefile (outputTemplate.OutputTemplate):
	def __init__(self, outputObject):
		outputTemplate.OutputTemplate.__init__(self, "makefile" ,"makefile")
		self.outputObject = outputObject

	def __del__(self):
		outputTemplate.OutputTemplate.__init__(self, filename).__del__(self)
		self.outputObject = None

	def getBuildFiles(self):
		return " ".join ("{name}.cpp".format(name = tableObj.getName()) for (tableName, tableObj) in self.outputObject.getTables().iteritems())

	def buildContents(self):
		dataMap = dict()
		dataMap["MAKEFILE_PROGRAM_NAME"] = "lib" + self.outputObject.getSchema().capitalize() + ".so"
		dataMap["MAKEFILE_FILES"] = self.getBuildFiles()
		self.loadTemplate()
		self.generateSourceCode(dataMap)