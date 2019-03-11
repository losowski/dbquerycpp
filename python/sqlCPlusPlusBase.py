#File to implement the C++ files
# Implements some functions to make building Functions easier

#import
import logging

class SQLCPlusPlusBase:
	def __init__(self, filename):
		self.fileName = filename
		pass

	def __del__(self):
		pass

	#Defines
	def fmt_def (self, name):
		return "{0}_HPP".format(name.upper().replace('.', '_'))

	def fmt_ifndefine (self, name):
		return "#ifndef {define}\n".format(define = self.fmt_def(name))

	def fmt_define (self, name):
		return "#define {define}\n".format(define = self.fmt_def(name))

	def fmt_endifdefine (self, name):
		return "#endif //{define}\n".format(define = self.fmt_def(name))

	#includes
	def fmt_include(self, library):
		return "#include \"{library}\"\n".format(library = library)

	def fmt_lib_include(self, library):
		return "#include <{library}>\n".format(library = library)

	#Use Namespace
	def useNamespace (self, namespace):
		return "using namespace {namespace};\n".format(namespace=namespace)

	def defineNamespace (self, namespace, content):
		return "namespace {namespace}\n{{\n\n{content}\n\n}}\n".format(namespace = namespace, content = content)

	#Typedef
	def fmt_typedef (self, knownType, customType):
		return "typedef {knownType} {customType}\n".format(knownType = knownType, customType = customType)

	#Function Parameters = list (type name)
	def functionArgs (self, parameters, templateDict = dict()):
		ret = str()
		logging.info("Parameters: %s", parameters)
		ret += ", ".join ("{name} {typeof}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (name, typeof) in parameters)
		return ret

	#Class Functions
	def className(self, className):
		return "class {className};\n\n".format(className = className)

	def classNameDefinition (self, className, derivedClass):
		return "class {className} : public {derivedClass}\n".format(className = className, derivedClass = derivedClass)

	#	Header
	def classFunctionTemplateHPP (self, ret, functionName, arguments, templateDict = dict()):
		return "{ret} {functionName}({arguments})".format(ret = ret.format(**templateDict), functionName = functionName.format(**templateDict), arguments = self.functionArgs(arguments, templateDict))

	def classFunctionHPP (self, ret, functionName, arguments, templateDict = dict()):
		return "{ret} {functionName}({arguments})".format(ret = ret, functionName = functionName, arguments = self.functionArgs(arguments))

	#	IMPL
	def classFunctionCPP (self, className, functionDetails):
		return "{ret} {className}::{functionName}({arguments})".format(ret = functionDetails[0], className= className, functionName = functionDetails[1], arguments = functionArgs(functionDetails[2]) )

	#List Functions
	# HEADER
	#	Constructor
	def constructorListHPP (self, className, constructors):
		val = "\tpublic:\n"
		for parameters in constructors:
			val += "\t\t{className} ({parameters});\n".format(className = className, parameters = self.functionArgs(parameters))
		val += "\t\t~{className} (void);\n".format(className = className)
		return val

	#	Function
	def functionListHPP(self, functions):
		val = "\tpublic:\n"
		for functionDetails in functions:
			val += "\t\t" + self.classFunctionHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2]) + ";\n"
		return val

	# Variables
	def classVariableHPP (self, variableType, variableName):
		return "\t\t{variableType}\t\t\t{variableName};\n".format(variableType = variableType, variableName = variableName)

	#Build the File
	#Overload this to build the actual file
	def buildContents(self):
		return str()

	def build(self):
		outputFile = open(self.fileName, 'w')
		#Build the output contents
		output = self.buildContents()
		#Write the File
		outputFile.write(output)
		outputFile.flush()
		outputFile.close()
