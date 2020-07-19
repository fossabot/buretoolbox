#!/usr/bin/env python3
""" Robots """

from ..plugin import BuretoolboxPlugin


class TestOutputPlugin(BuretoolboxPlugin):
    """ Various test output formats """
    def __init__(self):
        BuretoolboxPlugin.__init__(self)
        self.kind = "testoutput"

    def process(self):
        """ take the input and read them in """

    def finalize_reports(self):
        """ take the collected data and generate output """
