#SQL Create DB File Parser

#import
import logging
import re
import sqlSchemaBase
import sqlSchemaTable
import sqlSchemaTableColumn


class SQLSchemaFile (sqlSchemaBase.SQLSchemaBase):

	#SQL Non-commented line (must begin with a tab or alpha numeric
	nonCommentedLine = re.compile('^[A-Z\t \(\)]+')
	#Table Field Definitions
	TableFieldSQL = re.compile("\s?CREATE TABLE\s?(?P<table_name>\S+)\s+\((?P<field_definitions>.*)\).*;")
	#Get the column names
	ColumnNameSQL = re.compile("\s+(?P<column_name>\S+)\s+(?P<column_type>\S+)")
	#CONSTRAINTS
	PrimaryKeyConstraintSQL = re.compile("\s+CONSTRAINT\s?(?P<primary_key_name>\S+)\s?PRIMARY\s?KEY\s?\((?P<column_name>\S+)\)")
	ForeignKeyConstraintSQL= re.compile("\s+CONSTRAINT\s?(?P<foreign_key_name>\S+)\s?FOREIGN\s+KEY\s+\((?P<column_name>\S+)\)\s+REFERENCES\s+(?P<referenced_table>\S+)\s+\((?P<referenced_column>\S+)\).*")

	#TODO: Make the column code get all the columns

	def __init__(self, fileName):
		sqlSchemaBase.SQLSchemaBase.__init__(self, fileName)
		self.schemaFile = None
		self.tables = dict()	#	tableName - TableObj
		pass

	def __del__(self):
		sqlSchemaBase.SQLSchemaBase.__del__(self)
		pass

	def initialise(self):
		# Open file
		self.schemaFile = open(self.fileName, 'r')
		# Read in contents
		fileContents = self.schemaFile.readlines()

		sqlLine = str()
		for line in fileContents:
			#logging.debug("Line %s", line)
			reComment = self.nonCommentedLine.match(line)
			if (reComment != None):
				comment = reComment.group(0)
				logging.debug("Non-Commented Match: %s", line)
				#Build the SQLine
				#	remove tabs and linefeeds, and make the terminal ; into ;# for splitting
				sqlLine += line.replace('\t',' ').replace('\n',' ').replace(';',';#')
		#Now Split it into SQL Statements
		SQLStatements = sqlLine.split('#')
		for sqlStatement in SQLStatements:
			logging.debug("Statement: \"%s\"", sqlStatement)
			#Check if it really is SQL
			self.sqlParser(sqlStatement)
		# Close file
		self.schemaFile.close()

	def sqlParser(self, sqlStatement):
		#Check for create table lines
		if ("CREATE TABLE" in sqlStatement):
			#logging.info("CreateTableSQL: \"%s\"", comment)
			self.sqlParseCreateTable(sqlStatement)

	def sqlParseCreateTable (self, sqlStatement):
		logging.debug("CreateTable: \"%s\"\n", sqlStatement)
		#Get Table name
		tableFieldMatch = self.TableFieldSQL.match(sqlStatement)
		if (tableFieldMatch != None):
			tableName = tableFieldMatch.group('table_name')
			logging.debug("tableName: \"%s\"", tableName)
			#Create the table object
			tableObj = sqlSchemaTable.SQLSchemaTable(tableName)
			###
			### -- Other Field Definitions --
			###
			tableFieldDefinitions = tableFieldMatch.group('field_definitions')
			logging.debug("tableFieldDefinitions: \"%s\"", tableFieldDefinitions)
			#field_definitions split by comma
			for fieldData in tableFieldDefinitions.split(','):
				logging.debug("fieldData: \"%s\"", fieldData)
				#Run the ReGex for each identity
				primaryKeyConstraintSQLMatch = self.PrimaryKeyConstraintSQL.match(fieldData)
				ForeignKeyConstraintSQLMatch = self.ForeignKeyConstraintSQL.match(fieldData)
				columnNameMatch = self.ColumnNameSQL.match(fieldData)
				#Primary Key
				if (primaryKeyConstraintSQLMatch != None):
					logging.info("Primary Key Constraint: \"%s\"", fieldData)
					primaryKeyName = primaryKeyConstraintSQLMatch.group('primary_key_name')
					columnName = primaryKeyConstraintSQLMatch.group('column_name')
					logging.info("primaryKeyConstraintSQLMatch primaryKeyName: \"%s\"", primaryKeyName)
					logging.info("primaryKeyConstraintSQLMatch columnName: \"%s\"", columnName)
					tableObj.setPrimaryKey(columnName)
					continue
				#Foreign Key
				elif (ForeignKeyConstraintSQLMatch != None):
					logging.info("Foreign Key Constraint: \"%s\"", fieldData)
					foreignKeyName = ForeignKeyConstraintSQLMatch.group('foreign_key_name')
					columnName = ForeignKeyConstraintSQLMatch.group('column_name')
					referencedTable = ForeignKeyConstraintSQLMatch.group('referenced_table')
					referencedColumn = ForeignKeyConstraintSQLMatch.group('referenced_column')
					logging.info("ForeignKeyConstraintSQLMatch foreignKeyName: \"%s\"", foreignKeyName)
					logging.info("ForeignKeyConstraintSQLMatch columnName: \"%s\"", columnName)
					logging.info("ForeignKeyConstraintSQLMatch referencedTable: \"%s\"", referencedTable)
					logging.info("ForeignKeyConstraintSQLMatch referencedColumn: \"%s\"", referencedColumn)
					tableObj.addForeignKey(foreignKeyName, columnName, referencedTable,referencedColumn)
					continue
				#Failing above, check if a simple column definition
				# 	Matches pretty much everything!
				elif (columnNameMatch != None):
					logging.info("Field definition: \"%s\"", fieldData)
					#Proces Data
					columnName = columnNameMatch.group('column_name')
					columnType = columnNameMatch.group('column_type')
					logging.debug("columnNameMatch column_name: \"%s\"", columnName)
					if (columnName != 'CONSTRAINT'):
						logging.debug("columnNameMatch column_type: \"%s\"", columnType)
						tableObj.addColumn(columnName, columnType)
					else:
						logging.warning("Skipping column_name: \"%s\"", columnName)
				else:
					#This is Superfluous - it gets picked up in the fields regex anyway
					logging.error("Unhandled Constraint: \"%s\"", fieldData)
			#Store the table object
			self.tables[tableName] = tableObj

	def run(self):
		pass

	def getTables(self):
		return self.tables

	def shutdown(self):
		pass
