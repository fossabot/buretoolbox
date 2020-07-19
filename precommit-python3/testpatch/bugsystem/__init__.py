#!/usr/bin/env python3
""" Robots """

from ..reporting import ReportingPlugin


class BugsystemPlugin(ReportingPlugin):
    """ Project Definition """
    def __init__(self):
        ReportingPlugin.__init__(self)
        self.kind = "bugsystem"
        self.issue = None

    def locate_patch(self):
        """ find the patch based upon user input """

    def determine_branch(self):
        """ provide a branch hint """

    def determine_issue(self):
        """ set the bug system ID """

    def write_long_comment(self):
        """ write a longer text comment """

    def write_line_comment(self):
        """ pwrite a comment on a particular line """
