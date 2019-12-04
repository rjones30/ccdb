"""
      I S   E M P T Y   U T I L I T Y   E X A M P L E

Utilities provide commands for ccdb command like interface,
so if one runs:

  ccdb ls
  ccdb mkdir my_dir

'ls' and 'mk' are ccdb.cmd utilities.

Each utility represents one command and stored in one file.
The convention is that file name is the same as utility command.
So 'ls' is placed in 'ls.py'

All utilities are in:
$CCDB_HOME/python/ccdb/cmd/utils

CCDB discovers them automatically on start

Tip: When you develop your own utilities it is good idea to run ccdb
with flags:
 '--debug' (shows debug level messages)
 '--raise' (don't silents utility and ccdb exceptions)
"""
import logging
import os

import ccdb
import ccdb.path_utils
from ccdb.cmd import CliCommandBase, UtilityArgumentParser
from ccdb import AlchemyProvider
from ccdb import BraceMessage as LogFmt


#######################################################################
#                                                                     #
#             E M P T Y   U T I L I T Y (E X A M P L E)               #
#                                                                     #
#######################################################################

# logger must be set to ccdb.cmd.commands.<command name>
log = logging.getLogger("ccdb.cmd.commands.empty")


#*********************************************************************
#   Class Empty - empty utility example with description             *
#                                                                    *
#*********************************************************************
class Empty(CliCommandBase):
    """Empty utility example"""
    
    # ccdb command related attributes:

    command = "empty"
    name = "Empty"
    short_descr = "empty utility example"
    uses_db = True

    def __init__(self, context):
        super(Empty, self).__init__(context)
        self.raw_entry = "/"         # object path with possible pattern, like /mole/*

    #----------------------------------------
    #   cleanup
    #----------------------------------------
    def __cleanup(self):
        """Call this function in the beginning of command processing to prepare variables for new command"""
        self.raw_entry = "/"

    #
    #   process
    #----------------------------------------
    def execute(self, args):
        """This is an entry point for each time the command is called"""

        if log.isEnabledFor(logging.DEBUG):
            log.debug(LogFmt("{0}Empty is in charge{0}\\".format(os.linesep)))
            log.debug(LogFmt(" |- arguments : '" + "' '".join(args)+"'"))

        # prepare variables for the new command
        self.__cleanup()

        # get provider class which has functions for all CCDB database operation
        assert self.context
        provider = self.context.provider
        assert isinstance(provider, AlchemyProvider)

        # process arguments
        parsed_args = self.process_arguments(args)

        if not self.validate(parsed_args):
            return 1   # the return is like application ret. 1 means problems

        path = self.context.prepare_path(parsed_args.raw_path)   # add current path to user input

        # try avoid print() and use log to print data
        log.info(LogFmt("{0}raw_path{1}  : {2}", self.theme.Accent, self.theme.Reset, parsed_args.raw_path))
        log.info(LogFmt("{0}path{1}      : {2}", self.theme.Accent, self.theme.Reset, path))
        log.info(LogFmt("{0}variation{1} : {2}", self.theme.Accent, self.theme.Reset, parsed_args.variation))
        log.info(LogFmt("{0}run{1}       : {2}", self.theme.Accent, self.theme.Reset, parsed_args.run))
        log.info(LogFmt("{0}borders{1}   : {2}", self.theme.Accent, self.theme.Reset, parsed_args.show_borders))

        # Do something
        text = ""
        if parsed_args.show_borders:
            text = "+-------------------+\n" + \
                   "|   Empty command   |\n" + \
                   "+-------------------+\n"
        else:
            text = "Empty command"

        print(text)

        # return some data if we have it
        return text

#----------------------------------------
#   process_arguments 
#----------------------------------------  
    def process_arguments(self, args):
        #solo arguments

        #utility argument parser is argparse which raises errors instead of exiting app
        parser = UtilityArgumentParser()
        parser.add_argument("raw_path")
        parser.add_argument("-v", "--variation", default=self.context.current_variation)
        parser.add_argument("-r", "--run", default=self.context.current_run, type=int)

        # example of mutually exclusive group
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-b", "--borders", action="store_true", dest='show_borders', default=True)
        group.add_argument("-nb", "--no-borders", action="store_false", dest='show_borders')

        return parser.parse_args(args)

#----------------------------------------
#   validate 
#----------------------------------------  
    def validate(self, parsed_args):
        if not ccdb.path_utils.validate_name(parsed_args.raw_path):
            log.error("The wrong path is given")
            return False

        return True

#----------------------------------------
#   print_help 
#----------------------------------------
    def print_help(self):
        """Prints help for the command"""
        
        print ("""This is empty utility. It is a template and a sample for writing new utilities

    """)
