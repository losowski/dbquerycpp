#SQL Create DB File Parser

#import
import sys
import logging
import re
import sqlSchemaBase
import sqlSchemaTable
import sqlSchemaTableColumn


class SQLSchemaFile (sqlSchemaBase.SQLSchemaBase):
	#SQL Non-commented line (must begin with a tab or alpha numeric
	nonCommentedLine = re.compile('^[A-Z\t \(\)]+')
	#Schema Definition
	#	CREATE SCHEMA IF NOT EXISTS neuron_schema AUTHORIZATION neuron;
	SchemaSQL = re.compile("\s?CREATE\s+SCHEMA\s+IF\s+NOT\s+EXISTS\s+(?P<schema_name>\S+)\s+.*;")
	# SEQUENCE
	## CREATE SEQUENCE neuron_schema.tindividual_id_seq;
	SequenceSQL = re.compile("\s?CREATE\s+SEQUENCE\s+(?P<schema_name>\S+)\.(?P<sequence_name>\S+);")
	#Table Field Definitions
	TableFieldSQL = re.compile("\s?CREATE TABLE\s?(?P<table_name>\S+)\s+\((?P<field_definitions>.*)\).*;")
	SQLArray = re.compile("ANY\s?\(.*\)")
	#Get the column names
	ColumnNameSQL = re.compile("\s+(?P<column_name>\S+)\s+(?P<column_type>\S+)")
	ColumnNameSequenceSQL = re.compile("\s+(?P<column_name>\S+)\s+(?P<column_type>\S+).*nextval\((?P<column_sequence>\S+)::")
	#INDEX
	#CONSTRAINTS
	PrimaryKeyConstraintSQL = re.compile("\s+CONSTRAINT\s?(?P<primary_key_name>\S+)\s?PRIMARY\s?KEY\s?\((?P<column_name>\S+)\)")
	ForeignKeyConstraintSQL = re.compile("\s+CONSTRAINT\s?(?P<foreign_key_name>\S+)\s?FOREIGN\s+KEY\s+\((?P<column_name>\S+)\)\s+REFERENCES\s+(?P<referenced_table>\S+)\s+\((?P<referenced_column>\S+)\).*")
	# CREATE UNIQUE INDEX pk_body_name ON neuron_schema.tbody USING btree (name COLLATE pg_catalog."default") TABLESPACE pg_default;
	IndexSQL= re.compile("\s+CREATE\s+(?P<index_type>\S+)\s+INDEX\s+(?P<index_name>\S+)\s+ON\s+(?P<index_table>\S+).*\((?P<index_column>\S+)\).*;")

	#TODO: Make the column code get all the columns

	def __init__(self, fileName):
		sqlSchemaBase.SQLSchemaBase.__init__(self)
		self.logger = logging.getLogger('SQLSchemaFile')
		self.fileName		= fileName
		self.schemaFile		= None
		self.sequenceNames	= dict()

	def __del__(self):
		sqlSchemaBase.SQLSchemaBase.__del__(self)

	def loadData(self):
		# Open file
		self.schemaFile = open(self.fileName, 'r')
		# Read in contents
		fileContents = self.schemaFile.readlines()

		sqlLine = str()
		for line in fileContents:
			#self.logger.debug("Line %s", line)
			reComment = self.nonCommentedLine.match(line)
			if (reComment != None):
				comment = reComment.group(0)
				self.logger.debug("Non-Commented Match: %s", line)
				#Build the SQLine
				#	remove tabs and linefeeds, and make the terminal ; into ;# for splitting
				sqlLine += line.replace('\t',' ').replace('\n',' ').replace(';',';#')
		#Now Split it into SQL Statements
		SQLStatements = sqlLine.split('#')
		for sqlStatement in SQLStatements:
			self.logger.debug("Statement: \"%s\"", sqlStatement)
			#Check if it really is SQL
			self.sqlParser(sqlStatement)
		# Close file
		self.schemaFile.close()

	def sqlParser(self, sqlStatement):
		#Check for create table lines
		if ("CREATE TABLE" in sqlStatement):
			#self.logger.debug("CreateTableSQL: \"%s\"", comment)
			self.sqlParseCreateTable(sqlStatement)
		elif ("CREATE UNIQUE INDEX" in sqlStatement):
			#self.logger.debug("sqlParseCreateUniqueIndex: \"%s\"", comment)
			self.sqlParseCreateUniqueIndex(sqlStatement)
		elif ("CREATE INDEX" in sqlStatement):
			#self.logger.debug("sqlParseCreateIndex: \"%s\"", comment)
			self.sqlParseCreateIndex(sqlStatement)
		elif ("SEQUENCE" in sqlStatement):
			#self.logger.debug("sqlParseSequence: \"%s\"", comment)
			self.sqlParseSequence(sqlStatement)
		elif ("CREATE SCHEMA" in sqlStatement):
			#self.logger.debug("sqlParseCreateIndex: \"%s\"", comment)
			self.sqlParseCreateSchema(sqlStatement)

	def sqlParseCreateTable (self, sqlStatement):
		self.logger.debug("CreateTable: \"%s\"\n", sqlStatement)
		if "PRIMARY" not in sqlStatement:
			self.logger.critical("CREATE TABLE does not have a PRIMARY KEY defined: \"%s\"", sqlStatement)
			sys.exit(0)
		#Get Table name
		tableFieldMatch = self.TableFieldSQL.match(sqlStatement)
		if (tableFieldMatch != None):
			tableName = tableFieldMatch.group('table_name')
			self.logger.debug("tableName: \"%s\"", tableName)
			#Create the table object
			tableObj = sqlSchemaTable.SQLSchemaTable(tableName)
			# Retrieve relevant sequences
			seq = self.getSequence(tableName)
			logging.debug("Common Sequence: %s - %s", seq)
			tableObj.addSequences(seq)
			###
			### -- Other Field Definitions --
			###
			tableFieldDefinitions = tableFieldMatch.group('field_definitions')
			self.logger.debug("tableFieldDefinitions: \"%s\"", tableFieldDefinitions)
			#Remove the ARRAY
			CleanedTableFieldDefinitions = self.SQLArray.sub("", tableFieldDefinitions)
			self.logger.debug("tableFieldDefinitions2: \"%s\"", CleanedTableFieldDefinitions)
			#field_definitions split by comma
			for fieldData in CleanedTableFieldDefinitions.split(','):
				self.logger.debug("fieldData: \"%s\"", fieldData)
				#Run the ReGex for each identity
				primaryKeyConstraintSQLMatch = self.PrimaryKeyConstraintSQL.match(fieldData)
				ForeignKeyConstraintSQLMatch = self.ForeignKeyConstraintSQL.match(fieldData)
				columnNameMatch = self.ColumnNameSQL.match(fieldData)
				columnNameSequenceMatch = self.ColumnNameSequenceSQL.match(fieldData)
				#Primary Key
				if (primaryKeyConstraintSQLMatch != None):
					self.logger.debug("Primary Key Constraint: \"%s\"", fieldData)
					primaryKeyName = primaryKeyConstraintSQLMatch.group('primary_key_name')
					columnName = primaryKeyConstraintSQLMatch.group('column_name')
					self.logger.debug("primaryKeyConstraintSQLMatch primaryKeyName: \"%s\"", primaryKeyName)
					self.logger.debug("primaryKeyConstraintSQLMatch columnName: \"%s\"", columnName)
					tableObj.setPrimaryKey(columnName)
					continue
				#Foreign Key
				elif (ForeignKeyConstraintSQLMatch != None):
					self.logger.debug("Foreign Key Constraint: \"%s\"", fieldData)
					foreignKeyName = ForeignKeyConstraintSQLMatch.group('foreign_key_name')
					columnName = ForeignKeyConstraintSQLMatch.group('column_name')
					referencedTable = ForeignKeyConstraintSQLMatch.group('referenced_table')
					referencedColumn = ForeignKeyConstraintSQLMatch.group('referenced_column')
					self.logger.debug("ForeignKeyConstraintSQLMatch foreignKeyName: \"%s\"", foreignKeyName)
					self.logger.debug("ForeignKeyConstraintSQLMatch columnName: \"%s\"", columnName)
					self.logger.debug("ForeignKeyConstraintSQLMatch referencedTable: \"%s\"", referencedTable)
					self.logger.debug("ForeignKeyConstraintSQLMatch referencedColumn: \"%s\"", referencedColumn)
					tableObj.addForeignKey(foreignKeyName, columnName, referencedTable,referencedColumn)
					continue
				elif (columnNameSequenceMatch != None):
					self.logger.debug("Field definition: \"%s\"", fieldData)
					#Proces Data
					columnName = columnNameSequenceMatch.group('column_name')
					columnType = columnNameSequenceMatch.group('column_type').replace("\"","")
					columnSequence = columnNameSequenceMatch.group('column_sequence')
					self.logger.debug("columnNameSequenceMatch column_name: \"%s\"", columnName)
					self.logger.debug("columnNameSequenceMatch column_type: \"%s\"", columnType)
					self.logger.debug("columnNameSequenceMatch column_sequence: \"%s\"", columnSequence)
					if (columnName != 'CONSTRAINT'):
						self.logger.debug("columnNameMatch column_type: \"%s\"", columnType)
						columnObj = tableObj.addColumn(columnName, columnType)
						columnObj.setSequence(columnSequence)
					else:
						self.logger.warning("Skipping column_name: \"%s\"", columnName)
				#Failing above, check if a simple column definition
				# 	Matches pretty much everything!
				elif (columnNameMatch != None):
					self.logger.debug("Field definition: \"%s\"", fieldData)
					#Proces Data
					columnName = columnNameMatch.group('column_name')
					columnType = columnNameMatch.group('column_type').replace("\"","")
					self.logger.debug("columnNameMatch column_name: \"%s\"", columnName)
					self.logger.debug("columnNameMatch column_type: \"%s\"", columnType)
					if (columnName != 'CONSTRAINT'):
						self.logger.debug("columnNameMatch column_type: \"%s\"", columnType)
						tableObj.addColumn(columnName, columnType)
					else:
						self.logger.warning("Skipping column_name: \"%s\"", columnName)
				else:
					#This is Superfluous - it gets picked up in the fields regex anyway
					self.logger.error("Unhandled Constraint: \"%s\"", fieldData)
			#Store the table object
			self.tables[tableName] = tableObj



	def sqlParseCreateUniqueIndex (self, sqlStatement):
		self.sqlParseCreateIndex(sqlStatement)

	def sqlParseCreateIndex (self, sqlStatement):
		#	IndexSQL= re.compile("\s+CREATE\s+(?P<index_type>\S+)\s+INDEX\s+(?P<index_name>\S+)\s+ON\s+(?P<index_table>\S+).*\((?P<index_column>\S+).*;")
		IndexSQLMatch = self.IndexSQL.match(sqlStatement)
		#Primary Key
		if (IndexSQLMatch != None):
			self.logger.debug("Adding Indexes: \"%s\"", sqlStatement)
			indexType = IndexSQLMatch.group('index_type')
			indexName = IndexSQLMatch.group('index_name')
			indexTable = IndexSQLMatch.group('index_table')
			indexColumn = IndexSQLMatch.group('index_column')
			self.logger.debug("IndexSQLMatch indexType: \"%s\"", indexType)
			self.logger.debug("IndexSQLMatch indexName: \"%s\"", indexName)
			self.logger.debug("IndexSQLMatch indexTable: \"%s\"", indexTable)
			self.logger.debug("IndexSQLMatch indexColumn: \"%s\"", indexColumn)
			#Setup the known table with the index information
			self.tables[indexTable].addIndex(indexName, indexColumn)

	def sqlParseSequence (self, sqlStatement):
		#	SequenceSQL = re.compile("\s?CREATE\s+SEQUENCE\s+(?P<schema_name>\S+)\.(?P<sequence_name>\S+);")
		#	logging.debug("Sequence SQL: %s", sqlStatement)
		SequenceSQLMatch = self.SequenceSQL.match(sqlStatement)
		#Primary Key
		if (SequenceSQLMatch != None):
			self.logger.info("Adding Sequence: \"%s\"", sqlStatement)
			schemaName = SequenceSQLMatch.group('schema_name')
			sequenceName = SequenceSQLMatch.group('sequence_name')
			self.sequenceNames[sequenceName] = "{schema}.{sequence}".format(schema = schemaName, sequence=sequenceName)

	def getSequence(self, tableName):
		self.logger.debug("SchemaName: %s", self.getSchemaName())
		safeName = tableName.replace(self.getSchemaName()+".","")
		self.logger.debug("Safe table name : \"%s\"", safeName)
		sequenceDict = dict()
		for seq, seqSQL in self.sequenceNames.iteritems():
			if safeName in seq:
				sequenceDict[seq] = seqSQL
		self.logger.info("Found relevant sequences : \"%s\"", sequenceDict)
		return sequenceDict

	def sqlParseCreateSchema (self, sqlStatement):
		#	SchemaSQL = re.compile("\s?CREATE\s+SCHEMA\s+IF\s+NOT\s+EXISTS\s+(?P<schema_name>\S+)\s+.*;")
		SchemaSQLMatch = self.SchemaSQL.match(sqlStatement)
		#Primary Key
		if (SchemaSQLMatch != None):
			self.logger.info("Getting Schema name: \"%s\"", sqlStatement)
			schemaName = SchemaSQLMatch.group('schema_name')
			self.logger.error("SchemaSQLMatch schemaName: \"%s\"", schemaName)
			self.setSchema(schemaName)
