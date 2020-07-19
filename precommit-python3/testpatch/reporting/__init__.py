#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class ReportingPlugin(BuretoolboxPlugin):
    """ Project Definition """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "report"

    def write_finalreport(self):
        """ write the final report """
