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
		return "namespace {namespace}\n{{\n\n{content}\n\n}}\n".format(namespace = namespace, content=content)

	#Class Functions
	def classNameDefinition (self, className, derivedClass):
		return "class {className} : public {derivedClass}".format(className = className, derivedClass = derivedClass)

	def classScoping (self, className, functionDetails):
		return "{ret} {className}::{functionName} ({arguments})".format(ret = functionDetails[0], className= className, functionName = functionDetails[1], arguments = functionArgs(functionDetails[2]) )

	#Parameters = Ordered Dict (name, typeof)
	def functionArgs (self, parameters):
		ret = str()
		for name, typeof in parameters.iteritems():
			ret += "{typeof} {name}".format(name = name, typeof = typeof)
		return ret

	# Class HPP: functions : (scope, name, argument(s))
	def buildClassHPP(self, className, derivedClass, functions):
		pass



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
