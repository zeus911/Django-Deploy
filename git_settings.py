###  Git settings file for the deploy.py script
###  Options specified as dictionay key+values for the options dictionary,
###  and file is imported

###  This file wrappers the base options and settings used by the GIT
###  repository accessed by the deploy.py script for a site.  It assumes
###  that each stackdir is a separate code base, with a separate repository,
###  and that separate stackdirs will have separate deploy_settings.py and
###  git_settings.py files.

import os, sys

git_options = {}

# git_user is the user to use to access the Git repository.  Needs to be set
# for different users.
git_options['git_user'] = 'BenignCremator'
git_options['git_user_name'] = 'Hunter'
git_options['git_user_email'] = 'dracus@speakeasy.net'

# git_url is the default URL for git to access when cloning, pushing, etc
git_options['git_url'] = 'https://github.com/bethlakshmi/GBE2'

