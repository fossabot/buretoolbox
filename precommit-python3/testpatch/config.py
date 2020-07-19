#!/usr/bin/env python3

""" configuration file  """

import configparser
import os
import sys
from functools import partial

CONFIG_DEFAULT = {
    'basedir': os.getcwd(),
    'branch_default': 'main',
    'startdir': os.getcwd(),
    'configdir': os.path.join(os.path.expanduser('~'), '.config', 'buretoolbox'),
    'big_console_header_enabled': True,
    #'branch': None,
    'buildmode': 'patch',
    #'buildurl': None,
    #'buildconsole': None,
    'dirty_workspace': False,
    #'issue': None,
    'offline': False,
    #'patch_branch': None,
    'patch_branch_default': 'main',
    #'patch_naming_rule': None,
    #'patchfile': None,
    #'patchurl': None,
    'project': 'unknown',
    #'resetrepo': False,
    #'workdir': None,
    #'personality': None,
    'projectname': 'unknown',
    'relocate_workdir': False,
    'robot': False,
    'debug': False,
}

CONFIGFILE_DEFAULT = os.path.join(CONFIG_DEFAULT['configdir'], 'buretoolbox.ini')

RUNTIME_EXECUTABLES = ['git', 'rsync']

ERROR = partial(print, file=sys.stderr)

def verify_command(cmdname, cmdfile, showerror=True):
    """ verify a given executable is real """
    if not cmdfile and showerror:
        ERROR("ERROR: Executable for %s not specified." % (cmdname))
        return False

    cmdfile = find_file_in_path(cmdfile)
    if cmdfile:
        return True
    if showerror:
        ERROR("ERROR: No working %s found." % (cmdfile))
        return False
    return False

def test_verify_command():
    """ unit tests for verify_command """
    assert verify_command(cmdname='ls', cmdfile='ls', showerror=True)
    assert not verify_command(cmdname='ls', cmdfile='/asdfasdf/ls', showerror=True)
    assert verify_command(cmdname='ls', cmdfile='ls', showerror=False)
    assert not verify_command(cmdname='ls', cmdfile='/asdfasdf/ls', showerror=False)

def find_file_in_path(cmdfile):
    """ find a file in the user's path """
    if os.path.isabs(cmdfile):
        if os.path.isfile(cmdfile) and os.access(cmdfile, os.X_OK):
            return cmdfile
    for cmdpath in os.environ["PATH"].split(os.pathsep):
        exefile = os.path.join(cmdpath, cmdfile)
        if os.path.isfile(exefile) and os.access(exefile, os.X_OK):
            return exefile
    return None

def test_find_file_in_path():
    """ unit tests for find_file_in_path """
    assert find_file_in_path(cmdfile='ls')
    assert not find_file_in_path(cmdfile='/asdfasdf/ls')
    assert not find_file_in_path(cmdfile='asdfasdf')


class Config:
    """ configuration object """

    def __init__(self, filename=CONFIGFILE_DEFAULT):
        self.load_config(filename)

    def load_config(self, filename=CONFIGFILE_DEFAULT):
        """ create a new configuration from the given file """
        self.configparser = configparser.ConfigParser(defaults=CONFIG_DEFAULT)
        if os.path.exists(filename):
            self.configparser.read(filename)

    def dump_config(self, filename=None):
        """ dump the configuration to a file """
        if not filename:
            raise ValueError('No filename provided to config.dump_config.')

        tempparser = self.configparser
        tempparser.remove_section('RUNTIME')

        with open(filename, 'tw') as dump:
            tempparser.write(dump)

    def add_runtime_binary(self, binary=None):
        """ add an executable to the lookup dictionary """
        cmdfile = self.configparser.get('RUNTIME', binary)
        if not cmdfile:
            exefile = find_file_in_path(binary)
            if exefile:
                self.configparser.set('RUNTIME', binary, exefile)

    def set_runtime_defaults(self):
        """ set some defaults at runtime """
        for runtimes in RUNTIME_EXECUTABLES:
            self.add_runtime_binary(runtimes)
