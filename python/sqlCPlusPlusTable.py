#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusTable (sqlCPlusPlusBase.SQLCPlusPlusBase):
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							(
								("const string &", "connection",),
							),	#One constructor
						)

	#Schema templates - (ret, functionNametemplate, arguments)
	SCHEMA_FUNCTION_TEMPLATES =	(
									("p{tableName}", "g{tableName}", (
																			("int", "primaryKey"),
																		)
										),
								)
	def __init__(self, outputObject, filename):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__init__(self, filename)
		self.outputObject = outputObject


	def __del__(self):
		sqlCPlusPlusBase.SQLCPlusPlusBase.__del__(self)
		self.outputObject = None

	def tableFullName(self):
		return self.outputObject.getFullName()

	def tableName(self):
		return self.outputObject.getName()

	def schemaName(self):
		return self.outputObject.schemaName

	def buildContents(self):
		return str()

	# 	Class HPP: functions : (scope, name, argument(s))
	def buildClassHPP(self, className, derivedClass):
		ret = self.classNameDefinition(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		#TODO: Make functions
		ret += self.functionListHPP(self.SCHEMA_FUNCTION_TEMPLATES)
		ret += "}\n"
		return ret
