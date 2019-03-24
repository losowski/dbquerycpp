#File to implement the CPP file
# Uses data from the SQLSchemaTableBase


#import
import logging
import sqlCPlusPlusBase

class SQLCPlusPlusTable (sqlCPlusPlusBase.SQLCPlusPlusBase):
	#Ordered Dict (typeof, name)
	CONSTRUCTOR_ARGS =	(
							(
								("dbquery::DBConnection *", "connection",),
							),	#One constructor
							(
								("dbquery::DBConnection *", "connection",),
								("const int", "primaryKey"),
							),	#Two constructor

							(
								("dbquery::DBConnection *", "connection",),
								("int", "id"),
								("const string &", "text"),
							),	#Three constructor
						)

	CONSTRUCTOR_INIT_CPP =	(	#One constructor
								(
									("dbquery::DBConnection", ("connection",),),
								)
							),


	#Schema templates - (ret, functionNametemplate, arguments)
	TABLE_FUNCTION_TEMPLATES =	(
									("void", "selectRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																)
									),
									("void", "deleteRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																	("int", "primaryKey"),
																)
									),
									("void", "updateRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																)
									),
									("void", "insertRowSQL",	(
																	("shared_ptr<pqxx::work>", "txn"),
																)
									),
								)

	TYPEDEFS =	(
					("shared_ptr<{className}>", "p{className}"),
					("vector < p{className} >", "ap{className}"),
					("shared_ptr < ap{className}>", "pap{className}"),
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


	#Typedef
	def typedefListHPP(self, className):
		val = str()
		for typedefDetails in self.TYPEDEFS:
			val += self.fmt_typedef(knownType = typedefDetails[0].format(className = className), customType = typedefDetails[1].format(className = className))
		return val

	#Variables
	def classVariableListHPP(self):
		val = "\tpublic:\n"
		for columnName, columnObj in self.outputObject.getColumns().iteritems():
			val += self.classVariableHPP(variableType = columnObj.getType(), variableName = columnObj.getName())
		return val

	# Header
	# 	Class HPP: functions : (scope, name, argument(s))
	def buildTableClassHPP(self, className, derivedClass):
		ret = self.classNameDefinitionHPP(className, derivedClass)
		ret += "{\n"
		ret += self.constructorListHPP(className, self.CONSTRUCTOR_ARGS)
		#Functions
		ret += self.functionListHPP(self.TABLE_FUNCTION_TEMPLATES)
		#Variables
		ret += self.classVariableListHPP()
		ret += "}\n"
		return ret


	# Implementation
	#	Templated Table Functions
	def templatedNamedFunctionCPP (self, className, tableName, templateFunctions):
		val = str()
		for functionDetails in templateFunctions:
			val += self.classFunctionTemplateCPP(className = className, ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2], implementation = functionDetails[3], templateDict = {self.CONST_TABLENAME : tableName,})
		return val

	#templateFunctions = (ret, functionNametemplate, arguments)
	def templatedTableFunctionListCPP(self, className, templateFunctions):
		val = "//Functions to get single child objects\n"
		for idx, tableObj in enumerate(self.outputObject.tables.values()):
			val += "//{tableName}\n".format(tableName = tableObj.getName())
			val += self.templatedNamedFunctionCPP(className, tableObj.getName(), templateFunctions)
		return val


	# 	Class CPP: functions : (scope, name, argument(s))
	def buildTableClassCPP(self, className, constructors, constructionArgs, functions):
		ret = str()
		ret += self.constructorListCPP(className, constructors, constructionArgs)
		# Make Function implementations
		ret += self.templatedTableFunctionListCPP(className, functions)
		return ret
