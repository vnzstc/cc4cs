## Project Paths

PRJDIRNAME = $(notdir $(shell pwd))

PRJPATH=$(shell pwd)/
PRJ_INCLUDES_PATH=includes
PRJ_EXE_PATH=$(PRJPATH)exe
PRJ_HEX_PATH=$(PRJPATH)hex
PRJ_GCOV_PATH=$(PRJPATH)gcov
PRJ_ISASIM_PATH=$(PRJPATH)isasim

## Project options

PRGNAME=$(basename $(wildcard *.c))

PRJ_INCITINGS_DIRS=$(shell cd includes ; ls -d */ ; cd ..)
PRJ_INCITINGS=$(PRJ_INCITINGS_DIRS:/=)

## Project Items
SRC_C=$(PRGNAME).c
SRC_GCNO=$(PRGNAME).gcno

## Project Commands
CC=gcc
SDCC=sdcc
PACK=packihx
CC_GCOV=gcov
ISASIM=isasim

## Project Commands Options
CC_SRC=../../$(SRC_C)
CC_FLAGS= -fprofile-arcs -ftest-coverage
CC_INCLUDES= -I../../$(PRJ_INCLUDES_PATH) -I../../$(PRJ_INCLUDES_PATH)/$(incite)
CC_LIBS= -L/usr/lib/x86_64-linux-gnu/ -lm
CC_MACROS= -DCC

CC_DBG_FLAGS=
CC_DBG_MACROS=-DCC -DDEBUG

SDCC_SRC=../../$(SRC_C)
SDCC_OPT_FORGOT_OR_REMOVED= --noloopreverse --no-reg-params --peep-asm --peep-return --opt-code-size
SDCC_OPT_FLAGS_DISABLE= --nooverlay --nogcse --nolabelopt --noinvariant --noinduction --nojtbound
SDCC_OPT_FLAGS_PEEP= --no-peep --no-peep-return
SDCC_OPT_FLAGS_SPEED= --opt-code-speed
SDCC_OPT_FLAGS_LOSPRE= --nolospre --lospre-unsafe-read
SDCC_FLAGS= -mmcs51 --iram-size 128 $(SDCC_OPT_FLAGS_DISABLE) $(SDCC_OPT_FLAGS_PEEP) $(SDCC_OPT_FLAGS_SPEED) $(SDCC_OPT_FLAGS_LOSPRE)
SDCC_INCLUDES= -I../../$(PRJ_INCLUDES_PATH)/$(incite)
SDCC_LIBS=
SDCC_MACROS=-DI8051

GCOV_FLAGS=

## Debug Level Options and Commands

DBGLVL=0 #Set this variable to 0 to turn off debug printings.
debuglvl=if [ $(DBGLVL) -ge $(1) ] ; then echo  $(2) ; fi;

############# BUILDINGS COMMANDS ####

BUILDGCC_DBGLV=4
BUILDSDCC_DBGLV=4

DEBUG_GCC=$(call debuglvl, $(BUILDGCC_DBGLV), "Building " $(PRGNAME) " and " $(PRGNAME) "_debug in " $(PRJ_EXE_PATH)/$(incite)/)
DEBUG_SDCC=$(call debuglvl, $(BUILDSDCC_DBGLV), "Building " $(PRGNAME) ".ihx and " $(PRGNAME) ".hex in " $(PRJ_HEX_PATH)/$(incite)/)

BUILD_GCC=\
	$(CC) $(CC_SRC) $(CC_FLAGS) $(CC_INCLUDES) $(CC_LIBS) $(CC_MACROS) \
	-o $(PRGNAME)

BUILD_GCC_DEBUG=\
	$(CC) $(CC_SRC) $(CC_DBG_FLAGS) $(CC_INCLUDES) $(CC_LIBS) $(CC_DBG_MACROS) \
	-o $(PRGNAME)_debug

BUILD_SDCC=\
	$(SDCC) $(SDCC_SRC) $(SDCC_FLAGS) $(SDCC_INCLUDES) $(SDCC_LIBS) $(SDCC_MACROS)

BUILD_PACKIHX=\
	$(PACK) $(PRGNAME).ihx > $(PRGNAME).hex

############# BUILDINGS ENTRIES ####

build_gcc:
	@ $(foreach incite, $(PRJ_INCITINGS), cd $(PRJ_EXE_PATH)/$(incite)/ ; $(BUILD_GCC) ; $(BUILD_GCC_DEBUG) ; $(DEBUG_GCC) cd ./../../ ; )

build_sdcc:
	@ $(foreach incite,$(PRJ_INCITINGS), cd $(PRJ_HEX_PATH)/$(incite)/ ; $(BUILD_SDCC) ; $(BUILD_PACKIHX) ; $(DEBUG_SDCC) cd ./../../ ; )

############# STATISTICS GENERTATION COMMANDS ####

STATS_GCOV=\
	$(CC_GCOV) $(GCOV_FLAGS) $(SRC_GCNO)

STATS_ISASIM_DBG=\
	$(ISASIM) $(PRGNAME).hex $(PRGNAME)_DebugReport.txt > $(PRGNAME)_IsasimReport.txt

STATS_ISASIM=\
		$(ISASIM) $(PRGNAME).hex > $(PRGNAME)_IsasimReport.txt

############# STATISTICS GENERTATION ENTRIES ####

stats_gcov:
	@ $(foreach incite, $(PRJ_INCITINGS), cd $(PRJ_EXE_PATH)/$(incite)/ ; $(STATS_GCOV) ;  cd ./../../ ;)

stats_isasim:
	@ $(foreach incite, $(PRJ_INCITINGS), cd $(PRJ_HEX_PATH)/$(incite)/ ; $(STATS_ISASIM) ;  cd ./../../ ;)

############# INSTALLATION COMMANDS ####

INSTALL_GCOV_DBGLV=5
INSTALL_ISASIM_DBGLV=5

INSTALL_GCOV_GCNO_DEBUG= \

INSTALL_GCOV_GCNO=\
	 if [ -f $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).gcno ]; then \
		$(call debuglvl, $(INSTALL_GCOV_DBGLV), "Moving " $(PRGNAME).gcno " in " $(PRJ_GCOV_PATH)/$(incite)/ " directory")  \
		mv $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).gcno $(PRJ_GCOV_PATH)/$(incite) ; \
	 fi;

INSTALL_GCOV_GCDA=\
	 if [ -f $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).gcda ]; then \
		$(call debuglvl, $(INSTALL_GCOV_DBGLV), "Moving " $(PRGNAME).gcda " in " $(PRJ_GCOV_PATH)/$(incite)/ " directory") \
		mv $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).gcda $(PRJ_GCOV_PATH)/$(incite) ; \
	 fi;

INSTALL_GCOV_CGCOV=\
	 if [ -f $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).c.gcov ]; then \
		$(call debuglvl, $(INSTALL_GCOV_DBGLV), "Moving " $(PRGNAME).c.gcov " in " $(PRJ_GCOV_PATH)/$(incite)/ " directory") \
		mv $(PRJ_EXE_PATH)/$(incite)/$(PRGNAME).c.gcov $(PRJ_GCOV_PATH)/$(incite) ; \
	 fi;

INSTALL_ISASIM_DEBUGREPORT=\
	 if [ -f $(PRJ_HEX_PATH)/$(incite)/$(PRGNAME)_DebugReport.txt ]; then \
		$(call debuglvl, $(INSTALL_ISASIM_DBGLV), "Moving " $(PRGNAME)_DebugReport.txt " in " $(PRJ_ISASIM_PATH)/$(incite)/ " directory")  \
		mv $(PRJ_HEX_PATH)/$(incite)/$(PRGNAME)_DebugReport.txt $(PRJ_ISASIM_PATH)/$(incite) ; \
	 fi;

INSTALL_ISASIM_ISASIMREPORT=\
	 if [ -f $(PRJ_HEX_PATH)/$(incite)/$(PRGNAME)_IsasimReport.txt ]; then \
		$(call debuglvl, $(INSTALL_ISASIM_DBGLV), "Moving " $(PRGNAME)_IsasimReport.txt " in " $(PRJ_ISASIM_PATH)/$(incite)/ " directory")  \
		mv $(PRJ_HEX_PATH)/$(incite)/$(PRGNAME)_IsasimReport.txt $(PRJ_ISASIM_PATH)/$(incite) ; \
	 fi;

############# INSTALLATION ENTRIES ####

install:
	make install_gcov
	make install_isasim

install_gcov:
	@ $(foreach incite,$(PRJ_INCITINGS), $(INSTALL_GCOV_GCNO) )
	@ $(foreach incite,$(PRJ_INCITINGS), $(INSTALL_GCOV_GCDA) )
	@ $(foreach incite,$(PRJ_INCITINGS), $(INSTALL_GCOV_CGCOV) )

install_isasim:
	@ $(foreach incite,$(PRJ_INCITINGS), $(INSTALL_ISASIM_DEBUGREPORT) )
	@ $(foreach incite,$(PRJ_INCITINGS), $(INSTALL_ISASIM_ISASIMREPORT) )

############# CLEANING DIRECTORIES ENTRIES ####

CLEANDIR_DBGLV=5

cleandir: cleandir_files cleandir_exe cleandir_hex cleandir_gcov cleandir_isasim

cleandir_files:
	@ if [ -f $(PRGNAME)Report.txt ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_EXE_PATH) " directory") \
		rm $(PRGNAME)Report.txt -R ; \
	  fi;
	@ if [ -f $(PRGNAME)Report.csv ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_EXE_PATH) " directory") \
		rm $(PRGNAME)Report.txt -R ; \
	  fi;

cleandir_exe:
	@ if [ -d $(PRJ_EXE_PATH) ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_EXE_PATH) " directory") \
		rm $(PRJ_EXE_PATH) -R ; \
	  fi;
cleandir_hex:
	@ if [ -d $(PRJ_HEX_PATH) ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_HEX_PATH) " directory") \
		rm $(PRJ_HEX_PATH) -R ; \
	  fi;
cleandir_gcov:
	@ if [ -d $(PRJ_GCOV_PATH) ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_GCOV_PATH) " directory") \
		rm $(PRJ_GCOV_PATH) -R ; \
	  fi;
cleandir_isasim:
	@ if [ -d $(PRJ_ISASIM_PATH) ]; then \
		$(call debuglvl, $(CLEANDIR_DBGLV), "Deleting " $(PRJ_ISASIM_PATH) " directory") \
		rm $(PRJ_ISASIM_PATH) -R ; \
	  fi;

############# CHECKING DIRECTORIES COMMANDS ####

CHECKDIR_DBGLV=5
CHECKSUBDIR_DBGLV=$$(($(CHECKDIR_DBGLV)+1))

CHECKDIREXE= \
	if [ ! -d $(PRJ_EXE_PATH)/$(directory) ]; then \
		$(call debuglvl, $(CHECKSUBDIR_DBGLV), "Creating " $(PRJ_EXE_PATH)/$(directory) " directory") \
		mkdir $(PRJ_EXE_PATH)/$(directory) ; \
	fi;
CHECKDIRHEX= \
	if [ ! -d $(PRJ_HEX_PATH)/$(directory) ]; then \
		$(call debuglvl, $(CHECKSUBDIR_DBGLV), "Creating " $(PRJ_HEX_PATH)/$(directory) " directory") \
		mkdir $(PRJ_HEX_PATH)/$(directory) ; \
	fi;
CHECKDIRGCOV= \
	if [ ! -d $(PRJ_GCOV_PATH)/$(directory) ]; then \
		$(call debuglvl, $(CHECKSUBDIR_DBGLV), "Creating " $(PRJ_GCOV_PATH)/$(directory) " directory") \
		mkdir $(PRJ_GCOV_PATH)/$(directory) ; \
	fi;
CHECKDIRISASIM= \
	if [ ! -d $(PRJ_ISASIM_PATH)/$(directory) ]; then \
		$(call debuglvl, $(CHECKSUBDIR_DBGLV), "Creating " $(PRJ_ISASIM_PATH)/$(directory) " directory") \
		mkdir $(PRJ_ISASIM_PATH)/$(directory) ; \
	fi;

############# CHECKING DIRECTORIES ENTRIES ####

checkdir: checkdir_exe checkdir_hex checkdir_gcov checkdir_isasim

checkdir_exe_func:
	@$(call debuglvl, $(CHECKDIR_DBGLV), "Checkdir Trace: On!")

checkdir_exe:
	@ if [ ! -d $(PRJ_EXE_PATH) ]; then \
		$(call debuglvl, $(CHECKDIR_DBGLV), "Creating " $(PRJ_EXE_PATH) " directory") \
		mkdir $(PRJ_EXE_PATH); \
	  fi;
	@ $(foreach directory,$(PRJ_INCITINGS), $(CHECKDIREXE) )
checkdir_hex:
	@ if [ ! -d $(PRJ_HEX_PATH) ]; then \
		$(call debuglvl, $(CHECKDIR_DBGLV), "Creating " $(PRJ_HEX_PATH) " directory") \
		mkdir $(PRJ_HEX_PATH); \
	  fi;
	@ $(foreach directory,$(PRJ_INCITINGS), $(CHECKDIRHEX) )
checkdir_gcov:
	@ if [ ! -d $(PRJ_GCOV_PATH) ]; then \
		$(call debuglvl, $(CHECKDIR_DBGLV), "Creating " $(PRJ_GCOV_PATH) " directory") \
		mkdir $(PRJ_GCOV_PATH); \
	  fi;
	@ $(foreach directory,$(PRJ_INCITINGS), $(CHECKDIRGCOV) )
checkdir_isasim:
	@ if [ ! -d $(PRJ_ISASIM_PATH) ]; then \
		$(call debuglvl, $(CHECKDIR_DBGLV), "Creating " $(PRJ_ISASIM_PATH) " directory") \
		mkdir $(PRJ_ISASIM_PATH); \
	  fi;
	@ $(foreach directory,$(PRJ_INCITINGS), $(CHECKDIRISASIM) )
