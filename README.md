Django Deploy

Django Deploy is a deploy management script for use with Django
projects.  It will assist in managing code updates, making idependent
'stacks' for developement, code testing, etc, and backups of database
data.

Requirements 

*Python 2.6 or 2.7, but not (Yet!) 3.0
*Django 1.6
*GitPython 0.3

GitPython needs to be installed with either:
*ez_setup 0.9
*setuptools 5.4.1

or by using::
*pip 1.4.1

All version numbers are approximate

Yes, that is correct, you need to install two sepearate install
helpers just to install GitPython.  This can be partially automated
with the following command:

    wget https://bootstrap.pypa.io/ez_setup.py -O - | python

or by using:

    pip install gitpython

This is not even Beta code.  Do not use this unless you enjoy painful
bugs and hours wasted trying to figure out why unwritten code does not
run.  You have been warned.

