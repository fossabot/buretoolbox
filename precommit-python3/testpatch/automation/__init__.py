#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class AutomationPlugin(BuretoolboxPlugin):
    """ robots """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "automation"
        self.artifact_url = None
        self.consoleoutput = None

    def unittest_footer(self):
        """ additional info to add to the unit test footer output """

    def precheckout(self):
        """ operations to do prior to branch checkout """
