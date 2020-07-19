#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class TestToolPlugin(BuretoolboxPlugin):
    """ Plug-ins that test things """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "testtool"

    def filefilter(self, filename=None):
        """ process any file """

    def compile(self, repostatus):
        """ any work to do during compile step """

    def result(self, repostatus):
        """ generate results """

    def clean(self, repostatus):
        """ any work to do when cleaning the repo """

    def logfilter(self, repostatus):
        """ builds logs """

    def calcdiffs(self, repostatus):
        """ generate diffs between two logs """
