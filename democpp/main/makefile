# Contents based onL:
# https://www.cs.swarthmore.edu/~newhall/unixhelp/howto_makefiles.html

# master
# the compiler: gcc for C program, define as g++ for C++
CC = g++

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -std=c++17 -g -Wall

# define any directories containing header files other than /usr/include
#
INCLUDES = -I../../democpp

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
LFLAGS = -L../../lib -L/usr/lib/x86_64-linux-gnu

# define any libraries to link into executable:
#   if I want to link in libraries (libx.so or libx.a) I use the -llibname
#   option, something like (this will link in libmylib.so and libm.so:
#LIBS = -lliblog4cxx

# define the C source files- "main" is always last
SRCS = main.cpp

# define the C object files
#
# This uses Suffix Replacement within a macro:
#   $(name:string1=string2)
#         For each word in 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .c of all words in the macro SRCS
# with the .o suffix
#
OBJS = $(SRCS:.cpp=.o)

# define the executable file
MAIN = neuron_schema_test

#Subdirectory
#TOPTARGETS := all clean
#SUBDIRS = lib_html #lib_webpage

#
# The following part of the makefile is generic; it can be used to
# build any executable just by changing the definitions above and by
# deleting dependencies appended to the file from 'make depend'
#
.PHONY: depend clean

default: $(MAIN)

all: $(MAIN)
	echo "Web engine compiled"

$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

#PHONY: $(TOPTARGETS) $(SUBDIRS)

$(MAIN): $(OBJS)
	$(CC) $(CFLAGS) $(INCLUDES) -o $(MAIN) $(OBJS) $(LFLAGS) $(LIBS)

# this is a suffix replacement rule for building .o's from .c's
# it uses automatic variables $<: the name of the prerequisite of
# the rule(a .c file) and $@: the name of the target of the rule (a .o file)
# (see the gnu make manual section about automatic variables)
.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $<  -o $@

clean:
	rm $(OBJS) *~ $(MAIN)

depend: $(SRCS)
	makedepend $(INCLUDES) $^

install:
	cp $(MAIN) /var/www/cgi-bin/.

# DO NOT DELETE THIS LINE -- make depend needs it
