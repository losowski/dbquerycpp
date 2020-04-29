#!/usr/bin/python2
'''
Autogenerator script to read and build the CPP module
'''
#import
import logging
import time
import datetime

from python import sqlSchemaFile
#import signal

def main():
	print ("Autogenerator for DataBase CPP v0.01")
	#Build a datetime object with Current time
	dt = datetime.datetime.now()
	#Make the logging file
	loggingfile = "/tmp/buildDBcpp_{timestamp}.log".format(timestamp = dt.now().isoformat())
	#Setup logging
	logging.basicConfig(format='%(asctime)s\t%(name)-24s\t%(funcName)-24s\t[%(levelname)-8s] %(message)s', filename=loggingfile,level=logging.INFO)
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

