#File to implement the HPP file
# Uses data from the SQLSchemaTableBase

#import
import logging
import sqlCPlusPlusSchema

class SQLSchemaOutputHPP (sqlCPlusPlusSchema.SQLCPlusPlusSchema):
	TNAME = "tName"
	def __init__(self, outputObject):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__init__(self, outputObject, ".hpp")


	def __del__(self):
		sqlCPlusPlusSchema.SQLCPlusPlusSchema.__del__(self)


	def schemaInitialiseDataStructures(self):
		#Build the object constants
		#self.addClassScopeVariable(self.PUBLIC, "DBTransaction", "transaction") #public: DBTransaction		transaction;
		pass


	def tableInitialiseDataStructures(self, tableName, tableObj):
		#Build the object constants
		self.addClassScopeVariable(self.PRIVATE, "map{tName}".format(tName = tableObj.getName()), "{tName}Map".format(tName = tableObj.getName()))
		# Add the missing calls to addTypedefFormat - typedef	map < int , ptIndividual > maptIndividual;
		self.addTypedefFormat("map < int , p{tName} >", "map{tName}", {self.TNAME : tableObj.getName(),} )
		

	def buildContents(self):
		output = str()
		output += self.fmt_ifndefine(self.schemaName())
		output += self.fmt_define(self.schemaName())
		#Incldues
		output += self.fmt_include("dbconnection.hpp")
		output += self.fmt_include("dbtransaction.hpp")
		output += self.getTableIncludes()
		#Using Namespaces
		output += self.useNamespace("std")
		output += self.useNamespace("dbquery")
		#Code
		namespaced = str()
		#Build typedefs
		namespaced += self.buildTypedefs()
		#Build Class Functions
		namespaced += self.buildSchemaClassHPP(self.schemaName(), "dbquery::DBConnection")
		#Make a namespace
		output += self.defineNamespace(self.schemaName(), namespaced)
		output += self.fmt_endifdefine(self.schemaName())
		return output
