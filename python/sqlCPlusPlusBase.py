#File to implement the C++ files
# Implements some functions to make building Functions easier

#import
import logging

class SQLCPlusPlusBase:
	def __init__(self):
		pass

	def __del__(self):
		pass

	def fmt_include(self, library):
		return "#include \"%{library}\"".format(library = library)
