#!/usr/bin/env python

import os, sys

###  import of config stuff
from deploy_settings import *

exempt = dir()
exempt.append('exempt')
exempt.append('localcmds')

######  Put functions that CAN be used as commands from the command line
######  in this section.

def export_db(options):
    '''
    Exports a database from the named stack to the filename you provide.
    Accepts up to four arguments:
        stack - which stack you want to export from
        filename - filename the exported DB is saved to
        homedir - directory where export file is saved to
        project - the project to export the DB from, if unspecified,
            DB will be exported from all projects in the stack
        db_format - format of saved file, either json or xml
            (yaml is available if installed in the site python)
    '''
    
### These next two lines are as ugly as the sin of politics, but, wow,
### they would have made the code that follows so much cleaner
    for item in options.keys():
        exec(item+' = "'+options[item]+'"')

    savedir = options['savedir']
    stack = options['stack']
    stackdir = options['stackdir']
    filename = options['filename']

    if 'projects' not in options.keys() and 'project' in options.keys():
        projects = {options['project']: options['project']}
    elif 'projects' not in options.keys() and 'project' not in options.keys():
        projects = _get_stacks(stackdir+'/'+stack)
        if len(projects) != 0:
            project = projects[0]
        else: project = ""
        #projects = {stack: stack}
        #project = stack
    else:
        projects = options['projects']

    _check_dir(savedir)

    if 'db_format' not in options.keys():
        db_format = 'json'
    else:
        db_format = options['db_format']

    pwd = os.getcwd()
    if 'project' not in options.keys():
        os.chdir(stackdir+'/'+stack)
        sys.path.append(stackdir+'/'+stack)
        from stack_settings import projects
        for project in projects.keys():
            project_location = stackdir+'/'+stack+'/'+project
            _export(filename, db_format, project_location, projects[project]+'/stack_settings')

    else:
        project = options['project']
        project_location = stackdir+'/'+stack+'/'+project
        mod_location = project_location+'/manage.py'
        mod_settings_obj = _get_module_setting(mod_location)
        _export(savedir+'/'+filename, db_format, project_location, mod_settings_obj)
    os.chdir(pwd)
    
def import_db():
    '''
    Imports the database data contained in filename into the database.
    Accepts up to four arguments:
        stack - which stack you want to export from
        filename - filename the exported DB is saved to
        homedir - directory where export file is saved to
        db_format - format of saved file, either json or xml
            (yaml is available if installed in the site python)
    Not Completed.
    '''

    pass

def clear_db():
    '''
    Deletes the contents for a database of a stack.  Used to clear a database
    in preperation of importing new schema and data as part of a deploy process.
    '''
    
    pass

def pull_db():
    '''
    Pulls a DB file from our GitHub repository.  Requires the GitHub repository 
    be described in a conf file.
    Not completed.
    '''

    pass

def push_db():
    '''
    Pushes a DB file into our GitHub repository.  Requires the GitHub repository
    be described in a conf file.
    Not completed.
    '''

    pass

def pull_site():
    '''
    Pulls the site (project and app) code from our GitHub repository.  Requires 
    the GitHub repsoitory be describes in a conf file.  Accepts up to three 
    arugements:
        branch - the name of the branch to pull
        version - which version of the site code to pull
        stack - load the code into which stack, such as dev, test, stage, prod
            creates stack if it does not exist        
    Not completed.
    '''

    pass

def create_stack(options):
    '''
    Creates a stack (both the directory structure and config file) with the 
    provided name, and with provided options.  These include:
        port - specify the post to use [optional]
        project - project to start, if empty, skips
        app - application and setting filename in a project [optional]
            if empty, skips
        git_url - URL of the git respository to clone to populate the project
    Not completed.
    '''

    stackdir = options['stackdir']
    stack = options['stack']
    _check_dir(stackdir)
    if 'port_range' not in options.keys():
        options['port_range'] = '(8000, 8009)' 
    if stack not in _get_stacks(stackdir):    
        os.mkdir(stackdir+'/'+stack)
        os.mknod(stackdir+'/'+stack+'/stack_settings.py')

    ###  Need to put a call to manage.py to install a django project into 
    ###  a stack.  Need to decide how it is going to support multiple
    ###  projects in a stack, and importing from git/GitHub.

    os.chdir(stackdir+'/'+stack)
    if 'project' in options.keys():
        project = options['project']
        _add_project(stackdir+'/'+stack, project)
        if 'app' in options.keys():
            app = options['app']
            _add_app(stackdir+'/'+stack+'/'+project, app)
    elif 'git_url' in options.keys() or 'git' in options.keys():
        git = True
        if 'git_url' in options.keys():
            git_url = options['git_url']
        else:
            git_url = _git_options(homedir, 'baseurl')
        _git_clone(options, git_url)

    _populate_settings(stack, stackdir, options)

def delete_stack():
    '''
    Deletes the named stack, both the directory structure and the config file.  
    Will halt the app if it is currently running.
    Not completed.
    '''

    pass

######  End functions called from command line section.

localcmds = []
for cmd in dir():
	if cmd not in exempt:
	    localcmds.append(cmd)

######  Place function definitions that CAN NOT be used as commands from the
######  command line BELOW this line.

def _populate_settings(stack, stackdir, options = {'port_range': '(8000, 8010)'}):
    '''
    Add standard options into the [stack]/stack_settings.py file.
    '''

    ###  options_txt is a text blob that contains the default options and
    ###  comments for the [stack]/settings.py file.  Add a line to the file
    ###  by adding a line to the text blob.  Options within the file are
    ###  bracketted by percens, '%%...%%'.  The text between the percens 
    ###  is a dictionary keyword that replaces the token with its value.

    port = _free_port(options['port_range'], stackdir)
    options_txt = '''
###  Default options for the [stack]/settings.py file for each stack.
###  

###  port is the IP port that the server binds and listens to
port = '''+"'"+port+"'"+'''

'''

    if 'add_projects' in options.keys():
        options_txt = options_txt+'''
###  contains a dictionary of the projects within a stack as the keys,
###  and the name of the application settings file as the values

projects = {
'''

        if 'projects' in options.keys():
            if 'project' in options.keys():
                if 'app' in options.keys():
                    options['projects'] = {options['project']: options['app']} 
                else:
                    options['projects'] = {options['project']: options['project']}
        else : options['projects'] = {}
        for project in options['projects'].keys():
            options_txt = options_txt+"    '"+project+"': '"+options['projects'][project]+"',"

        options_txt = options_txt+'''
    }
'''

    _write_file(stackdir+'/'+stack+'/stack_settings.py', options_txt)

def _write_file(filename, text):
    '''
    Write (output) a file.  Provide filename with complete path, and a
    text blob.
    '''

    file = open(filename, 'w+')
    file.write(text)
    file.close

def _get_stacks(stackdir):
    '''
    Gets the list of stacks currently configured on the system.  If given
    path of a stack, gets projects within that stack.
    '''
    stacks = []
    for file in os.listdir(stackdir):
        if os.path.isdir(stackdir+'/'+file):
            stacks.append(file)
    return stacks

def _check_dir(dir):
    '''
    Check that the directory [dir] exists, and creates it if it does
    not.  For managing the tmp, save, and stack directories.
    '''
    if not os.path.isdir(dir) and not os.path.isfile(dir):
        os.mkdir(dir)
        os.chmod(dir, 0755)

def _get_module_settings(mod_location):
    '''
    Gets the project and module settings location from the stack
    manage.py file
    '''

    ###  This is a fugly way of doing this.  Rethink this and find an
    ###  more elegant way to get this done.

    with open(mod_location, 'r') as file:
        for line in file:
            if 'os.environ.setdefault' in line and 'DJANGO_SETTINGS_MODULE' in line:
                return line.split()[1][1:-2]
    file.close()

def _export(filename, db_format, location, mod_settings_obj):
    '''
    Export function, handles the call to the django management core
    '''

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", mod_settings_obj)
    from django.core.management import execute_from_command_line

    os.chdir(location)
    sys.path.append(location)
    sys.argv = ['manage.py', 'dumpdata', '--format', db_format]
    #sys.argv = ['manage.py', 'dumpdata', '--output', filename, '--format', db_format]
    execute_from_command_line(sys.argv)

def _add_project(stack_dir, project):
    '''
    Creates the project infrastructure, projects.py files and populates it 
    with the projects within the stack.  If app is specified, also creates it.
    '''

    from django.core.management import execute_from_command_line
    execute_from_command_line(['django-admin.py', 'startproject', project])
    
    stack = stack_dir.split('/')[-1]
    stackdir = stack_dir[0:-(1+len(stack))]
    project_file = stackdir+'/stack_settings'

def _add_app(stack_dir, app):
    '''
    Add an app to a project.  
    '''

    pwd = os.getcwd()
    stack = stack_dir.split('/')[-1]
    stackdir = stack_dir[0:-(1+len(stack))]
    os.chdir(stackdir)

    from django.core.management import execute_from_command_line
    cmd = ['django-admin.py', 'startapp', app]
    execute_from_command_line(cmd)

    os.chdir(pwd)

def _git_clone(options, git_url):
    '''
    Clone a Git repository into a directory structure based on a Git URL.
    Accepts the usual Git options, see the git_settings.py file.
    '''

    print options
    import git

    locations = []

    if 'cfgdir' in options.keys():
        location.append(options['cfgdir']+'/git_settings.py')
    if 'homedir' in options.keys():
        location.append(options['homedir']+'/git_settings.py')
    if 'stackdir' in options.keys():
        locations.append(options['stackdir']+'/git_settings.py')
    if 'stack' in options.keys():
        locations.append(options['stackdir']+'/'+stack+'/git_settings.py')
    new_options = _get_git_options(locations)

    for option in new_options.keys():
        git_options[option] = new_options[options]
    del new_options, locations

    repo = git.Repo.init(stack, bare = True)
    assert repo.bare == True
    clone = repo.clone(git_url)

def _get_git_options(locations):
    '''
    Returns the git options from the git_settings file for a stack.  Accepts
    either stack name, or ordered list of potential git_settings.py files.  
    Each entry in list overwrites previous options, allowing each layer to
    only change the settings from the previous layer.
    '''

    options = {}

    for file in locations:
        if os.isfile(file):
            exec('from '+file+' import git_options')
            for option in git_options.keys():
                options[option] = git_options[option]
    return options

def _free_port(port_range, stackdir):
    '''
    Checks which ports are free, check first the stack, then if the port
    has a connection on it.  Returns first port from range.  
    '''

    if type(port_range) == type('text'):
        exec('port_range = '+port_range)
    ports = range(port_range[0], port_range[1])
    pwd = os.getcwd()
    for stack in _get_stacks(stackdir):
        os.chdir(stackdir+'/'+stack)
        sys.path.append(stackdir+'/'+stack)
        print stackdir+'/'+stack
        try: from stack_settings import port
        except: port = False
        sys.path.remove(stackdir+'/'+stack)

        if type(port) == type('text'):
            exec('port = '+port)
        if port in ports:
            ports.remove(port)
    os.chdir(pwd)

    for port in ports:
        if _check_port(port) == False:
          return str(port)

def _check_port(port):
    '''
    Check if the port is in use, by seeing if there is a process, pipe, etc
    connected to it.  If there is, return True, if not, return False.
    '''

    import socket
    testport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        testport.bind(('localhost', port))
    except:
        return True
    testport.close()
    return False

helpstring = [
    '''
    Usage: deploy.py command [stack] [[option1] [parameter1] 
        [option2] [parameter2]...]

    A deploy script to help manage django projects.  Assists with
    importing and exporting database files, pulling a project down
    from GitHub (with help of appropriate configuration files), etc.

    It introduces the concept of stacks to django projects.  A stack
    is a directory structure that contains a django project, and some
    deploy.py specific config files.  It is inspired by the DevOps
    stacks (dev, test, staging, production), and are assumed to be
    used in a similar fashion, with each stack being an independent
    installation for a specific purpose.  The name of the stack should
    reflect that purpose.  Eventually, the deploy.py script will
    support specifying branches and versions for the code base and
    database installed within a stack.  
    This is not complete yet.
    ''', 

    '''
    The deploy.py script can also be used in the same manner as the
    manage.py script.  Just specify stack, then the usual manage.py
    commands and options as normal: 
        python deploy.py test runserver 8001 
    Multiple stacks can be specified as a tuple:
	    python deploy.py (test, stage, prod) create_stack
    ''', 

    ''' 
    The options can be used in this fashion are as follows: 
    ''',

    ]

if len(sys.argv) == 1:
    print helpstring[0]
    print
    print "Local commands:"
    for cmd in localcmds:
        print cmd+":"
        exec('print '+cmd+'.__doc__')
        print
    print helpstring[2]
    from django.core.management import execute_from_command_line
    execute_from_command_line()

elif sys.argv[1] in localcmds:
    cmd = sys.argv[1]
    options['stack'] = sys.argv[2]
    for argv in range(0, len(sys.argv[3:])/2):
        options[sys.argv[3+(argv*2)]] = sys.argv[4+(argv * 2)]
    call = globals()[cmd]
    call(options)

#elif __name__ == "__main__":
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deploy_settings")

#    from django.core.management import execute_from_command_line

#    sys.argv[0]='django-admin.py'
#    execute_from_command_line(sys.argv)
