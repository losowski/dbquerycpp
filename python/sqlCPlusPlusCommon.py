#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusCommon (sqlCPlusPlusBase.SQLCPlusPlusBase):
	def __init__(self, outputObject, filename):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.logger = logging.getLogger('SQLCPlusPlusCommon')
		self.outputObject = outputObject

	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def getSafeTypeConversion(self, tableObject, objectReference = str()):
		val = str()
		for columnName, columnData in tableObject.getColumns().iteritems():
			self.logger.debug("getSafeTypeConversion column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\tdbquery::DBSafeUtils::safeTo{datatype}(&{objectRef}{column}, res[i][\"{column}\"]);\n".format(column = columnName, datatype = columnData.getCPPSafeType(), objectRef= objectReference)
		return val

	def getTypeConversion(self, tableObject, objectReference = str()):
		val = str()
		for columnName, columnData in tableObject.getColumns().iteritems():
			self.logger.debug("getTypeConversion column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\tdbquery::DBUtils::to{datatype}(&{objectRef}{column}, res[i][\"{column}\"]);\n".format(column = columnName, datatype = columnData.getCPPSafeType(), objectRef= objectReference)
		return val

	#under_scored_name to underScoredName
	def formatName(self, inputName):
		self.logger.debug("Format In: %s", inputName)
		output = ''.join( word.title() for word in inputName[1:].replace("id_seq","").split("_"))
		self.logger.debug("Format: %s", output)
		return output

