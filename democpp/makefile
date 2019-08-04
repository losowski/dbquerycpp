# MAKEFILE for thie libhtml library

###############
# DEFINITIONS #
###############
# BASE DIRECTORY for install (/usr/local is good)
BASE_PREFIX = /usr/local
MAN_BASE_PREFIX = $(BASE_PREFIX)/share/man

# #DEFINE: These go into CFLAGS later
#OTHER1 -D_NAME_YOUR_DEFINE=99


######################
# SYSTEM DEFINITIONS #
######################
INSTALL= install
RM= rm -rf
MKDIR = mkdir -p

###########
# INSTALL #
###########

# MAKE FILE VERSIONING
# VERSION
include Makefile.inc/VERSION

#MANUAL DEFINITIONS
# MAN_EXT No idea what this means
MAN_EXT=1


#BUILDING DEFINITIONS
BIN_DIR=$(BASE_PREFIX)/bin
LIB_DIR=$(BASE_PREFIX)/lib
MAN_DIR=$(MAN_BASE_PREFIX)/man$(MAN_EXT)

INSTALL_PROGRAM_PERM=$(INSTALL) -c -m 0755 #readable and executable by anyone, writing restricted to user owner
INSTALL_DATA_PERM = $(INSTALL) -c -m 0644 #readable by anyone. Writable by user owner


###
## LOCAL BUILD ##
###
LOCAL_BASE_PREFIX = ..
LOCAL_MAN_BASE_PREFIX = $(LOCAL_BASE_PREFIX)/share/man
LOCAL_BIN_DIR=$(LOCAL_BASE_PREFIX)/bin
LOCAL_LIB_DIR=$(LOCAL_BASE_PREFIX)/lib
LOCAL_MAN_DIR=$(LOCAL_MAN_BASE_PREFIX)/man$(MAN_EXT)

###############
# COMPILATION #
###############
#Compiler (gcc or g++)
CC ?= g++

TARGET_FLAG = -shared -fPIC -std=c++11
#Compiler options (i.e. pedantic etc -g = adds debugging)
COMPILER_OPTIONS = -g -Wall

#Compiler flags - and include the Makefile.inc/VERSION (VERSION)
CFLAGS = $(TARGET_FLAG) $(COMPILER_OPTIONS) -DVERSION=\"$(VERSION)\" #Other definitions $(OTHER1)

###################
## PROJECT FILES ##
###################
PROGRAM_NAME=libdemo.so
#INCLUDES
INCLUDES = -I../libdbquery

#Libraries
LDFLAGS = -L/usr/lib/x86_64-linux-gnu -L../lib -ldbquery

#Soures
SRCS = tbody.cpp tindividual.cpp neuronschema.cpp

###########
## MAGIC ##
###########
OBJECT_FILES = $(SRCS:.cpp=.o)

####################
# MAKEFILE SCRIPTS #
####################

default: $(PROGRAM_NAME)
 
all: $(PROGRAM_NAME)

$(PROGRAM_NAME): $(OBJECT_FILES)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(PROGRAM_NAME) $(OBJECT_FILES)

installdirs:
	#test -d $(DESTDIR)$(BIN_DIR) || $(MKDIR) $(DESTDIR)$(BIN_DIR)
	test -d $(DESTDIR)$(LIB_DIR) || $(MKDIR) $(DESTDIR)$(LIB_DIR)
	#test -d $(DESTDIR)$(MAN_DIR) || $(MKDIR) $(DESTDIR)$(MAN_DIR)

install: $(PROGRAM_NAME) installdirs
	#$(INSTALL_PROGRAM_PERM)	$(PROGRAM_NAME)   $(DESTDIR)$(BIN_DIR)/$(PROGRAM_NAME)
	$(INSTALL_PROGRAM_PERM)	$(PROGRAM_NAME)   $(DESTDIR)$(LIB_DIR)/$(PROGRAM_NAME)
	#$(INSTALL_DATA_PERM)		$(PROGRAM_NAME).$(MAN_EXT) $(DESTDIR)$(MAN_DIR)/$(PROGRAM_NAME).$(MAN_EXT)

# Local Install (build directories)
local_installdirs:
	#test -d $(LOCAL_BIN_DIR) || $(MKDIR) $(LOCAL_BIN_DIR)
	test -d $(LOCAL_LIB_DIR) || $(MKDIR) $(LOCAL_LIB_DIR)
	#test -d $(LOCAL_MAN_DIR) || $(MKDIR) $(LOCAL_MAN_DIR)

local_install: $(PROGRAM_NAME) local_installdirs
	#$(INSTALL_PROGRAM_PERM)	$(PROGRAM_NAME)   $(LOCAL_BIN_DIR)/$(PROGRAM_NAME)
	$(INSTALL_PROGRAM_PERM)	$(PROGRAM_NAME)   $(LOCAL_LIB_DIR)/$(PROGRAM_NAME)
	#$(INSTALL_DATA)		$(PROGRAM_NAME).$(MAN_EXT) $(LOCAL_MAN_DIR)/$(PROGRAM_NAME).$(MAN_EXT)

#No idea what this adds
.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $<  -o $@

clean:
	$(RM) $(OBJECT_FILES)
	$(RM) $(PROGRAM_NAME)

