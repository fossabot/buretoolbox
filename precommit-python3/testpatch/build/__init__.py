#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class BuildPlugin(BuretoolboxPlugin):
    """ define a build tool """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "build"
        self.buildfile = "buildfile.txt"

    def executor(self):
        """ execute the build command """

    def module_params(self, repostatus=None, testname=None):
        """ default parameters for each test type """
