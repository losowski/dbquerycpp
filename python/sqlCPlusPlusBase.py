#File to implement the C++ files
# Implements some functions to make building Functions easier

#import
import logging

class SQLCPlusPlusBase:
	#Datatype conversion
	SQLDATATYPEDEFAULT	=	"string"
	SQLDATATYPEMAPPING	=	{
							'bigint'	:	'int',
							'char'		:	'string',
							'text'		:	'string',
							'timestamp'	:	'string',
						}
	PRIVATE		=	"private"
	PROTECTED	=	"protected"
	PUBLIC		=	"public"

	def __init__(self, filename):
		self.logger = logging.getLogger('SQLCPlusPlusBase')
		self.fileName = filename.lower()
		self.classVariables = dict() # dict(scope : dict(variable, type))
		self.typedefs = list() # (knownType, customType)
		self.staticVariable = dict() #  scope : dict[variableName] = list (varType, value)

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

	def addTypedef (self, knownType, customType):
		self.typedefs.append( (knownType, customType) )

	def addTypedefFormat(self, knownTypeFormat, customTypeFormat, formatDict):
		knownType = knownTypeFormat.format(**formatDict)
		customType = customTypeFormat.format(**formatDict)
		self.addTypedef(knownType, customType)

	def buildTypedefs (self):
		ret = str()
		for knownType, customType in self.typedefs:
			ret += self.fmt_typedef(knownType, customType)
		return ret

	#Function Parameters = list (type name)
	#HOWTO:
	#	1)	All typeof, and name should be either a value or a formattable string (i.e either "value" or "{value}")
	#	2)	All templateDict items should be KEYS (i.e only "key"). If you put in "{key}" it WILL BREAK
	def functionArgs (self, parameters, templateDict = dict()):
		ret = str()
		self.logger.debug("functionArgs parameters: %s", parameters)
		self.logger.debug("functionArgs templateDict: %s", templateDict)
		ret += ", ".join ("{typeof} {name}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (typeof, name,) in parameters)
		return ret

	#Class Functions
	def className(self, className):
		return "class {className};\n\n".format(className = className)

	def classNameDefinitionHPP (self, className, derivedClass):
		return "class {className} : public {derivedClass}\n".format(className = className, derivedClass = derivedClass)

	#	Header
	## Header Functions
	def classFunctionTemplateHPP (self, keyword, ret, functionName, arguments, templateDict = dict()):
		if (None == keyword):
			keyword = ""
		return "\t\t{keyWord} {ret} {functionName}({arguments});\n".format(keyWord = keyword, ret = ret.format(**templateDict), functionName = functionName.format(**templateDict), arguments = self.functionArgs(arguments, templateDict))

	def classFunctionHPP (self, keyword, ret, functionName, arguments, templateDict = dict()):
		if (None == keyword):
			keyword = ""
		return "\t\t{keyWord} {ret} {functionName}({arguments});\n".format(keyWord = keyword, ret = ret, functionName = functionName, arguments = self.functionArgs(arguments))

	# Class variables list
	# Allow addition of class variables with scopes
	def addClassScopeVariable(self, variableScope, variableType, variableName):
		scoped = self.classVariables.setdefault(variableScope, dict())
		scoped[variableName] = variableType

	# Engine function to add the variables
	def classScopeVariableHPP(self):
		retVal = str()
		for variableScope, variableList in self.classVariables.iteritems():
			retVal += "\t{scope}:\n".format(scope = variableScope)
			for variableName, variableType  in variableList.iteritems():
				retVal += "\t\t{vType}\t\t\t\t\t{vName};\n".format(vType = variableType, vName = variableName)
		return retVal

	def classVariableHPP (self, variableType, variableName):
		return "\t\t{variableType}\t\t\t{variableName};\n".format(variableType = self.SQLDATATYPEMAPPING.get(variableType, self.SQLDATATYPEDEFAULT), variableName = variableName)

	#Static Variable (static const)
	def addStaticVariable(self, scope, varType, variableName, value):
		scoped = self.staticVariable.setdefault(scope, dict())
		scoped[variableName] = (varType, value)
		pass

	def staticVariableHPP(self):
		retVal = str()
		for variableScope, variableList in self.staticVariable.iteritems():
			retVal += "\t{scope}:\n".format(scope = variableScope)
			for variableName, variableDetails  in variableList.iteritems():
				variableType, variableValue = variableDetails
				retVal += "\t\tstatic const {vType}\t{vName};\n".format(vType = variableType, vName = variableName, vValue = variableValue)
		return retVal

	#	IMPL
	def staticVariableCPP(self, className):
		retVal = str()
		for variableScope, variableList in self.staticVariable.iteritems():
			for variableName, variableDetails  in variableList.iteritems():
				variableType, variableValue = variableDetails
				retVal += "const {vType}\t{vClass}::{vName} ({vValue});\n\n".format(vType = variableType, vName = variableName, vValue = variableValue, vClass = className)
		return retVal



	#	IMPL
	def classFunctionTemplateCPP (self, className, ret, functionName, arguments, implementation, templateDict = dict()):
		return "{ret} {className}::{functionName}({arguments})\n{{\n{functionContent}\n}}\n\n".format(
				className = className,
				ret = ret.format(**templateDict),
				functionName = functionName.format(**templateDict),
				arguments = self.functionArgs(arguments, templateDict),
				functionContent = implementation.format(**templateDict)
			)

	def classFunctionCPP (self, className, functionDetails):
		return "{ret} {className}::{functionName}({arguments})".format(ret = functionDetails[0], className= className, functionName = functionDetails[1], arguments = functionArgs(functionDetails[2]) )

	def templatedFunctionCPP(self, templateString, table):
		return templateString.format(tableName = table)

	#List Functions
	# HEADER
	#	Constructor
	def constructorListHPP (self, className, constructorsTemplate, templateDict = dict()):
		val = "\tpublic:\n"
		for constructor in constructorsTemplate:
			parameters = constructor[0]
			val += self.constructorHPP(className, parameters, templateDict)
		#TODO: Add constructor for same type
		return val

	def constructorHPP (self, className, parameters, templateDict):
		return "\t\t{className} ({parameters});\n".format(className = className, parameters = self.functionArgs(parameters, templateDict))

	#Destructor to follow constructor
	def destructorHPP (self, className):
		val = "\tpublic:\n"
		val += "\t\t~{className} (void);\n\n".format(className = className)
		return val

	#Constructor List
	def parameterList (self, parameterList, templateDict = dict()):
		self.logger.debug("parameterList: %s", parameterList)
		ret = ", ".join ("{name}".format(name = name.format(**templateDict)) for name in parameterList)
		self.logger.debug("parameterList output: %s", ret)
		return ret


	def constructorBuilder(self, classConstructors, templateDict):
		self.logger.debug("classConstructors: %s", classConstructors)
		buildObjects = list()
		#Construct the build objects
		for construct in classConstructors:
			objectName = construct[0]
			self.logger.debug("objectName construct: %s", objectName)
			initArgs = construct[1]
			self.logger.debug("initArgs construct: %s", initArgs)
			buildObjects.append ( (objectName, initArgs) )
		#	ret += ", ".join ("{typeof} {name}".format(name = name.format(**templateDict), typeof = typeof.format(**templateDict)) for (typeof, name,) in parameters)
		return ",\n\t".join("{objectName} ({initArgs})".format(objectName = objectName.format(**templateDict), initArgs = self.parameterList(initArgs, templateDict) ) for (objectName, initArgs) in  buildObjects)

	def constructorListCPP (self, className, constructorsTemplate, templateDict = dict()):
		val = str()
		#Get Constructor functions
		for constructor in constructorsTemplate:
			self.logger.debug("constructor: %s", constructor)
			#Get Arguments for constructor
			parameters = constructor[0]
			constructionArgs = constructor[1]
			self.logger.debug("parameters: %s", parameters)
			self.logger.debug("constructionArgs: %s", constructionArgs)
			val += self.constructorCPP(className, parameters, constructionArgs, templateDict)
		return val

	def constructorCPP (self, className, parameters, constructionArgs, templateDict):
		return "{className}::{className} ({parameters}):\n\t{init}\n{{\n}}\n\n".format(	className = className,
																						parameters = self.functionArgs(parameters, templateDict),
																						init = self.constructorBuilder(constructionArgs, templateDict))

	def destructorCPP (self, className):
		return "{className}::~{className} (void)\n{{\n}}\n\n".format(className = className)

	#	Function
	def functionListHPP(self, functions):
		val = "\tpublic:\n"
		for functionDetails in functions:
			val += self.classFunctionHPP(keyword = functionDetails[0], ret = functionDetails[1], functionName = functionDetails[2], arguments = functionDetails[3])
		return val

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
