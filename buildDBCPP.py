#!/usr/bin/python
'''
Autogenerator script to read and build the CPP module
'''
#import
import logging
from python import sqlSchemaFile
#import signal

def main():
	print ("Autogenerator for DataBase CPP v0.01")
	logging.basicConfig(format='%(asctime)s\t%(name)-16s\t%(funcName)-16s\t[%(levelname)-8s] %(message)s', filename='/tmp/buildDBcpp.log',level=logging.DEBUG)
	sqlSchema = sqlSchemaFile.SQLSchemaFile('database.sql')
	sqlSchema.loadData()
	sqlSchema.initialise()
	sqlSchema.initialiseDataStructures()
	sqlSchema.build()
	#Signal handler needed here to wait before exiting
	#sigset = [signal.SIGINT, signal.SIGTERM]
	#signal.sigwait(sigset) #3.3 only
	#signal.pause()
	#Finally shutdown the server
	sqlSchema.shutdown()
	print("Exiting...")


# Assign a start point to the executable
if __name__ == "__main__":
	main()

