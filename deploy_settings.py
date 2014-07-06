###  Settings file for the deploy.py script
###  Options specified as dictionay key+values for the options dictionary,
###  and file is imported

import os, sys

#  options is a container dictionary.  All setting variables are placed
#  inside of it, and it gets punted around like a football.
options = {}

#  homedir is the home directory everything else is relative to
#options['homedir'] = os.getcwd()
options['homedir'] = '/home/dracus/Projects'

#  savedir is the directory exported files are saved to, or imported
#  files are imported from.  Usually, a temporary file area.
options['savedir'] = options['homedir']+'/save'

#  stackdir is the directory that stacks are stored under.  Has a
#  separate directory structure for isolation.  Each directory under
#  this directory is a separate stack.  There is also a settings file
#  for each stack in this directory, of the name '[stack]_settings.py'.
#  The settings files are imported options for that stack.
options['stackdir'] = options['homedir']+'/stack'

#  format is the output format for db exports.  Can be json or xml,
#  rarely can by yaml
options['db_format'] = 'json'

#  filename is the file name for any number of optional files, usually
#  the file used for DB exports and imports
options['filename']  = 'db-export.json'

#  stack is the default stack to work upon.  Normally, this is reset at
#  the command line
options['stack'] = 'test'

#  project is the default project to work upon.  Normally, this is reset
#  at the command line
#options['project'] = 'test_project'

#  app is the default app to work upon.  Normally, this is specified at
#  the command line
#options['app'] = 'test_app'
