#File to implement the C++ files
# Implements some functions to make building Functions easier

#import
import logging

class SQLCPlusPlusBase:
	#Datatype conversion
	SQLDATATYPEMAPPING	=	{
							'bigint'	:	'int',
							'char'		:	'char',
							'text'		:	'string',
							'timestamp'	:	'string',
						}

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
		return "#include \"{library}\"\n".format(library = library.lower())

	def fmt_lib_include(self, library):
		return "#include <{library}>\n".format(library = library)

	#Use Namespace
	def useNamespace (self, namespace):
		return "using namespace {namespace};\n".format(namespace=namespace)

	def defineNamespace (self, namespace, content):
		return "namespace {namespace}\n{{\n\n{content}\n\n}}\n".format(namespace = namespace, content = content)

	#Typedef
	def fmt_typedef (self, knownType, customType):
		return "typedef {knownType} {customType};\n".format(knownType = knownType, customType = customType)

	#Function Parameters = list (type name)
	def functionArgs (self, parameters, templateDict = dict()):
		ret = str()
		#logging.debug("functionArgs: %s", parameters)
		ret += ", ".join ("{typeof} {name}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (typeof, name,) in parameters)
		return ret

	#Class Functions
	def className(self, className):
		return "class {className};\n\n".format(className = className)

	def classNameDefinitionHPP (self, className, derivedClass):
		return "class {className} : public {derivedClass}\n".format(className = className, derivedClass = derivedClass)

	#	Header
	def classFunctionTemplateHPP (self, ret, functionName, arguments, templateDict = dict()):
		return "{ret} {functionName}({arguments})".format(ret = ret.format(**templateDict), functionName = functionName.format(**templateDict), arguments = self.functionArgs(arguments, templateDict))

	def classFunctionHPP (self, ret, functionName, arguments, templateDict = dict()):
		return "\t\t{ret} {functionName}({arguments});\n".format(ret = ret, functionName = functionName, arguments = self.functionArgs(arguments))

	#	IMPL
	def classFunctionTemplateCPP (self, className, ret, functionName, arguments, implementation, templateDict = dict()):
		return "{ret} {className}::{functionName}({arguments})\n{{\n{functionContent}\n}}\n\n".format(className = className, ret = ret.format(**templateDict), functionName = functionName.format(**templateDict), arguments = self.functionArgs(arguments, templateDict), functionContent = implementation.format(**templateDict))

	def classFunctionCPP (self, className, functionDetails):
		return "{ret} {className}::{functionName}({arguments})".format(ret = functionDetails[0], className= className, functionName = functionDetails[1], arguments = functionArgs(functionDetails[2]) )

	def templatedFunctionCPP(self, templateString, table):
		return templateString.format(tableName = table)

	#List Functions
	# HEADER
	#	Constructor
	def constructorListHPP (self, className, constructorsTemplate):
		val = "\tpublic:\n"
		for constructor in constructorsTemplate:
			parameters = constructor[0]
			val += "\t\t{className} ({parameters});\n".format(className = className, parameters = self.functionArgs(parameters))
		val += "\t\t~{className} (void);\n".format(className = className)
		return val


	#Constructor List
	def parameterList (self, parameterList):
		logging.debug("parameterList: %s", parameterList)
		ret = ", ".join ("{name}".format(name = name) for name in parameterList)
		logging.debug("parameterList output: %s", ret)
		return ret


	def constructorBuilder(self, classConstructors):
		logging.debug("classConstructors: %s", classConstructors)
		ret = str()
		for construct in classConstructors:
			objectName = construct[0]
			logging.debug("objectName construct: %s", objectName)
			initArgs = construct[1]
			logging.debug("initArgs construct: %s", initArgs)
			ret += "{objectName} ({initArgs})".format(objectName = objectName, initArgs = self.parameterList(initArgs) )
		logging.info("constructorBuilder output: %s", ret)
		return ret

	def constructorListCPP (self, className, constructorsTemplate):
		val = str()
		#Get Constructor functions
		for constructor in constructorsTemplate:
			logging.info("constructorsTemplate constructor: %s", constructor)
			#Get Arguments for constructor
			parameters = constructor[0]
			constructionArgs = constructor[1]
			logging.info("parameters: %s", parameters)
			logging.info("constructionArgs: %s", constructionArgs)
			val += "t{className}::{className} ({parameters}):\n\t{init}\n{{\n}}\n\n".format(className = className, parameters = self.functionArgs(parameters), init = self.constructorBuilder(constructionArgs))
		val += "~{className}::{className} (void)\n{{\n}}\n".format(className = className)
		return val

	#	Function
	def functionListHPP(self, functions):
		val = "\tpublic:\n"
		for functionDetails in functions:
			val += self.classFunctionHPP(ret = functionDetails[0], functionName = functionDetails[1], arguments = functionDetails[2])
		return val

	# Variables
	def classVariableHPP (self, variableType, variableName):
		return "\t\t{variableType}\t\t\t{variableName};\n".format(variableType = self.SQLDATATYPEMAPPING.get(variableType,'string'), variableName = variableName)

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
