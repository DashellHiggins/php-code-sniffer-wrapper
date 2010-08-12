# Run php code sniffer, but ignore chosen warnings (for use on Linux)
# Author: Dashell Higgins ( http://github.com/DashellHiggins )
#!/usr/bin/python
import os
import sys
import subprocess

# Print error messages about the following:
flags = {
    #### General style ####
    "Line exceeds 85 characters" :                              "hide",
    "Opening brace" :                                           "hide",
    "Expected \"foreach (...) {" :                              "",
    "Expected \"while (...) {" :                                "",
    "Expected \"if (...) {" :                                   "",
    "There must be a single space between the closing parenthesis and the opening brace of a multi-line .* statement" : "",

    #### Document level documentation ####
    "You must use \"/**\" style comments for a file comment" :  "",
    "one blank line before the tags in file comment" :          "hide",
    "PHP version not specified" :                               "hide",
    "Missing @\w* tag in file comment" :                        "hide",
    "Missing class doc comment" :                               "hide",
    "Missing @\w* tag in class comment" :                       "hide",

    #### Function level documentation ####
    "must use \"/**\" style comments for a function comment" :  "",
    "one blank line before the tags in function comment" :      "hide",
    "Missing function doc comment" :                            "",
    "Missing comment for param \"" :                            "hide",
    "The variable names for parameters .* do not align" :       "hide",
    "The comments for parameters .* do not align" :             "hide",
    "Doc comment for .* does not match actual variable name" :  "hide",
    "Missing @return tag in function comment" :                 "hide",

    }

def prune_output(command, flags):
    '''Prune the output by adding a series of pipes to grep -v and hiding warnings that the user want to ignore'''
    for excluded_string, show in flags.items():
        if show == "hide":
            command = command + " | grep -v '" + excluded_string + "'"
    #finally, remove the dashed lines from the output, and the line giving the (incorrect) number of errors/warnings
    command = command + " | grep -v '\-\-\-\-\-\-' | grep -v 'AFFECTING [0-9]* LINE(S)'"
    return command

#execute on the specified file, otherwise print usage
if (len(sys.argv) > 1):
    var = subprocess.call("php -l " + sys.argv[1] + " | grep -v 'No syntax errors detected'", shell=True)
    #set the report width so that errors are not split over lines
    command = prune_output("phpcs --report-width=200 " + sys.argv[1], flags)
    subprocess.call(command, shell=True)

else:
    print "PHP code sniffer wrapper.  This script calls phpcs, but excludes warnings deemed bothersome or unimportant.  Usage:\npython phpcs_wrapper.py [file]\nSet preferences by editing phpcs_wrapper.py"


