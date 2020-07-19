#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class Maven(BuretoolboxPlugin):
    """ define a build tool """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "build"
        self.buildfile = "pom.xml"
        self.buildtool = 'maven'
