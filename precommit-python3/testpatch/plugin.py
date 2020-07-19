#!/usr/bin/env python3
""" Plug-in Objects """


class BuretoolboxPlugin():
    """ Basic BuretoolboxPlugin """
    def __init__(self):
        self.kind = "undefined"
        self.description = "Short description"
        self.identifier = "shortname"  # 10 characters or less

    def usage(self):
        """ process command line arguments """

    def parse_args(self):
        """ process command line arguments """

    def initialize(self):
        """ perform any plug-in initialization """

    def precheck(self):
        """ prechecks """

    def docker_support(self):
        """ handle any container support """

    def patchfile(self, patchfile=None):
        """ operations on the actual patch file """

    def precompile(self, repostatus):
        """ prior to compile step work """

    def postcompile(self, repostatus):
        """ after compilation has happened """

    def rebuild(self, repostatus):
        """ anything that rebuilds the source tree """

    def postcleanup(self):
        """ any cleanup required prior to exiting """
