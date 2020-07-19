#!/usr/bin/env python3

""" base class and handler for plugins """

from abc import abstractmethod
import inspect
import os
import re
import pkgutil
import sys
sys.dont_write_bytecode = True

import config

class YetusPlugin(object):
    def __init__(self, ):
        self.description = 'what it does'

    @abstractmethod
    def set_defaults(self, name=None, defaults=None):
        if name not in yetus.config:
            self.set_overrides(name=name, overrides=defaults)
        else:
            for k in list(defaults.keys()):
                if k not in yetus.config[name]:
                    yetus.config[name].update({k: defaults[name].get(k)})

    @abstractmethod
    def set_overrides(self, name=None, overrides=None):
        for k1 in overrides:
            if isinstance(overrides[k1], dict):
                if k1 not in yetus.config:
                    yetus.config.update({k1: overrides.get(k1)})
                else:
                    for k2 in list(overrides[k1].keys()):
                        yetus.config[k1].update({k2: overrides[k1].get(k2)})
            else:
                yetus.config.update({k1: overrides.get(k1)})

    @abstractmethod
    def remove_plugin(self, name=None):
        if not name:
            return False

        del self.plugins[name]
        return True

    @abstractmethod
    def create_args(self):
        pass

    @abstractmethod
    def parse_args(self, args):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def docker_support(self):
        pass

    @abstractmethod
    def file_test(self, filename=None):
        pass


class BugSystem(YetusPlugin):
    @abstractmethod
    def finalreport(self,
                    result=1,
                    header=None,
                    votes=None,
                    tests=None,
                    footer=None):
        pass

    @abstractmethod
    def importplugins(self, idir=None):
        bg = re.compile('yetusplugins\.bugsystems\.')

        for module in list(sys.modules.keys()):
            classname = re.sub('yetusplugins\.bugsystems\.', '', module)
            if bg.match(module) and classname != 'bugsystems':
                try:
                    m = importlib.import_module(module)
                    self.plugins[classname] = getattr(m, classname +
                                                      'BugSystem')()
                    yetus.debug('Importing bugsystem %s: %sBugSystem' %
                                (m, classname))
                except Exception as e:
                    yetus.debug('Importing %s bugsystem: %s' % (classname, e))

    @abstractmethod
    def determine_branch(self):
        return False

    @abstractmethod
    def determine_issue(self, issue=None):
        return False

    @abstractmethod
    def locate_patch(self, inputdata=None, filename=None):
        return False

    @abstractmethod
    def write_comment(self, filename=None):
        pass


class CommonBuild(YetusPlugin):
    @abstractmethod
    def prechecks(self):
        return True

    @abstractmethod
    def calcdiffs(self, branchlog=None, patchlog=None):
        pass

    @abstractmethod
    def logfilter(self, loginput=None, logoutput=None):
        pass

    @abstractmethod
    def precompile(self, repostatus='patch'):
        return True

    @abstractmethod
    def compile(self, repostatus='patch'):
        return True

    @abstractmethod
    def postcompile(self, repostatus='patch'):
        return True

    @abstractmethod
    def rebuild(self, repostatus='patch'):
        return True

    @abstractmethod
    def patchfile(self, filename=None):
        pass

    @abstractmethod
    def distclean(self):
        return True


class Test(CommonBuild):
    @abstractmethod
    def importplugins(self, idir=None):
        bg = re.compile('yetusplugins\.tests\.')

        for module in list(sys.modules.keys()):
            classname = re.sub('yetusplugins\.tests\.', '', module)
            if bg.match(module) and classname != 'tests':
                try:
                    m = importlib.import_module(module)
                    self.plugins[classname] = getattr(m, classname + 'Test')()
                    yetus.debug("Importing test: %sTest" % (classname))
                except Exception as e:
                    #yetus.debug("Importing test: %s" % (e))
                    pass

    @abstractmethod
    def compile(self, repostatus='patch'):
        return True

    @abstractmethod
    def paramlist(self, buildtool=None):
        return None

    @abstractmethod
    def test(self):
        return True


class TestFormat(CommonBuild):
    @abstractmethod
    def importplugins(self, idir=None):
        bg = re.compile('yetusplugins\.testformats\.')

        for module in list(sys.modules.keys()):
            classname = re.sub('yetusplugins\.testformats\.', '', module)
            if bg.match(module) and classname != 'testformats':
                try:
                    m = importlib.import_module(module)
                    self.plugins[classname] = getattr(m, classname +
                                                      'TestFormat')()
                    yetus.debug("Importing testformat: %sTestFormat" %
                                (classname))
                except Exception as e:
                    #yetus.debug("Importing testformat: %s" % (e))
                    pass

    @abstractmethod
    def process_tests(self,
                      module=None,
                      test_logfile=None,
                      fnfrag=None,
                      multijdk=None):
        pass

    @abstractmethod
    def finalize_results(self, multijdk=None):
        pass

    @abstractmethod
    def prechecks(self):
        pass


class BuildTool(CommonBuild):
    @abstractmethod
    def importplugins(self, idir=None):
        bg = re.compile('yetusplugins\.buildtools\.')

        for module in list(sys.modules.keys()):
            classname = re.sub('yetusplugins\.buildtools\.', '', module)
            if bg.match(module) and classname != 'buildtools':
                try:
                    m = importlib.import_module(module)
                    self.plugins[classname] = getattr(m, classname +
                                                      'BuildTool')()
                    yetus.debug("Importing buildtool: %sBuildTool" %
                                (classname))
                except Exception as e:
                    #print("Importing buildtool: %s" % (e))
                    pass

    @abstractmethod
    def reorder_modules(self, repostatus='patch'):
        pass

    @abstractmethod
    def executor(self):
        pass

    @abstractmethod
    def module_worker(self, repostatus='patch', testtype=None):
        pass

    @abstractmethod
    def reorder_modules(self, repostatus='patch', changed=None, parent=None):
        pass


class Personality(CommonBuild):
    @abstractmethod
    def module(self, repostatus='patch', testtype=None):
        pass
