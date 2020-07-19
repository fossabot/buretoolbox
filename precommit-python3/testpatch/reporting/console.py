#!/usr/bin/env python3

""" Write report output to the screen """

from . import ReportingPlugin


class Console(ReportingPlugin):
    """ class to write a formatted text report to the screen """

    def __init__(self):
        ReportingPlugin.__init__(self)
        self.description = "Generate test report to the console"
        self.identifier = "consoletxt"
        self.console_report_file = None

    def write_finalreport(self):
        print("output")

    def parse_args(self):
        self.console_report_file = "filename"

    def docker_support(self):
        if self.console_report_file:
            print("Do something")
