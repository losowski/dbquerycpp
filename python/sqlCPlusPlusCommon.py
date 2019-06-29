#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusCommon (sqlCPlusPlusBase.SQLCPlusPlusBase):
	def __init__(self, outputObject, filename):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.outputObject = outputObject

	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def getSafeTypeConversion(self, tableObject, objectReference = str()):
		val = str()
		for columnName, columnData in tableObject.getColumns().iteritems():
			logging.info("getSafeTypeConversion column: \"%s\" - \"%s\"", columnName, columnData.getType())
			val += "\t\tdbquery::DBSafeUtils::safeTo{datatype}(&{objectRef}{column}, res[i][\"{column}\"]);\n".format(column = columnName, datatype = columnData.getCPPSafeType(), objectRef= objectReference)
		return val
