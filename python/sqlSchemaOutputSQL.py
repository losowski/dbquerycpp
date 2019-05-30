#File to implement the SQL file
# Uses data from the SQLSchemaTableBase

#import
import logging
import outputTemplate

class sqlSchemaOutputSQL (outputTemplate.OutputTemplate):
	def __init__(self, outputObject):
		outputTemplate.OutputTemplate.__init__(self, "procedures.sql" , "database/"+outputObject.tableName+"_procedures.sql")
		self.outputObject = outputObject
		self.schemaName = self.outputObject.getSchemaName()
		self.tableName = self.outputObject.tableName.lower()
		self.nonPKColumns = list()

	def __del__(self):
		outputTemplate.OutputTemplate.__del__(self)
		self.outputObject = None

	def __setNonPKColums(self):
		for columnName, columnData in self.outputObject.getColumns().iteritems():
			if columnName != self.outputObject.getPrimaryKey():
				self.nonPKColumns.append(columnName)
				logging.debug("ColumnCheck \"%s\"", columnName)
			else:
				logging.debug("ColumnCheck PK \"%s\"", columnName)


	#Functions to populate the data
	#	SQL_INPUT_PARAMETERS
	def __storedProcInputParameter(self, columnName):
		# IN	p_name				neuron_schema.tBody.name%TYPE default NULL
		return "\tIN\tp_{COLUMN_NAME}\t{SQL_SCHEMANAME}.{SQL_TABLENAME}.{COLUMN_NAME}%TYPE default NULL".format(SQL_SCHEMANAME = self.schemaName, SQL_TABLENAME = self.tableName, COLUMN_NAME = columnName)

	def buildStoredProcInputParameters(self):
		return ",\n".join ("{inputParameter}".format(inputParameter = self.__storedProcInputParameter(columnName)) for columnName in self.nonPKColumns)

	# SQL_DECLARED_PK
	def __storedProcDeclared(self, columnName):
		#	v_id					neuron_schema.tBody.id%TYPE := NULL;
		return "\tv_{COLUMN_NAME}\t\t{SQL_SCHEMANAME}.{SQL_TABLENAME}.{COLUMN_NAME}%TYPE := NULL;".format(SQL_SCHEMANAME = self.schemaName, SQL_TABLENAME = self.tableName, COLUMN_NAME = columnName)

	def buildStoredProcDeclared(self):
		return self.__storedProcDeclared(self.outputObject.getPrimaryKey())

	#	SQL_PRIMARY_KEY
	def buildPrimaryKey(self):
		return self.outputObject.getPrimaryKey()

	#	SQL_COLUMNS
	def buildColums(self):
		return ",\n\t\t\t".join (self.nonPKColumns)

	#	SQL_VALUES
	def buildColumValues(self):
		return ",\n\t\t\t".join ("p_{inputParameter}".format(inputParameter = columnName) for columnName in self.nonPKColumns)


	def build(self):
		# Functions
		self.__setNonPKColums()
		# Build the map
		dataMap = dict()
		dataMap["SQL_TABLENAME"] = self.tableName
		dataMap["SQL_SCHEMANAME"] = self.schemaName
		dataMap["SQL_INPUT_PARAMETERS"] = self.buildStoredProcInputParameters()
		dataMap["SQL_DECLARED_PK"] = self.buildStoredProcDeclared()
		# TODO: Add SQL column / query definitions
		dataMap["SQL_PRIMARY_KEY"] = self.buildPrimaryKey()
		dataMap["SQL_COLUMNS"] = self.buildColums()
		dataMap["SQL_VALUES"] = self.buildColumValues()
		# Process the template
		self.loadTemplate()
		self.generateSourceCode(dataMap)
