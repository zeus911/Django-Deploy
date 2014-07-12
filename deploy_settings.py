###  Settings file for the deploy.py script
###  Options specified as dictionay key+values for the options dictionary,
###  and file is imported

###  This file wrappers the base options and settings used by the deploy.py
###  deploy.py script for a site.  It assumes that each homedir is a separate
###  code base, with a separate repository, and that separate stackdirs will
###  have separate deploy_settings.py and git_settings.py files.  Also
###  assumes that the user is calling the file from either the homedir or
###  below, or from a common bin area for the user, with the settings files
###  in a .deploy.py directory in the users home directory.

import os, sys

#  options is a container dictionary.  All setting variables are placed
#  inside of it, and it gets punted around like a football.
options = {}

#  homedir is the home directory everything else is relative to
#options['homedir'] = os.getcwd()
options['homedir'] = '/home/gbeahost/deploy_area'

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

#  cfgdir is a central directory for settings and configuration files
#  only set it if you create one
if os.path.isdir(os.environ['HOME']+'/.django-deploy'):
    options['cfgdir'] = os.environ['HOME']+'/.django-deploy'

