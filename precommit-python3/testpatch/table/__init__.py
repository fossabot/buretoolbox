#!/usr/bin/env python3

""" Display tables """

import sys
sys.dont_write_bytecode = True


class DisplayTable():
    """ Generic table object """
    def __init__(self):
        self.table = []

    def add(self, desc=None, content=None):
        """ add an entry """
        self.table.append({desc: content})

    def finish(self):
        """ last minute touches """

class HeaderTable(DisplayTable):
    """ what a header looks like """

    def __init__(self):
        DisplayTable.__init__(self)

class VoteTable(DisplayTable):
    """ what a vote table looks like """

    def __init__(self):
        DisplayTable.__init__(self)

    def add(self, desc=None, content=None):
        """ add an entry """
        self.vote(vote='0', testname=desc, text=content)

    def vote(self, vote='0', testname=None, timer=None, text=None):
        """ add a vote """
        if vote in ('1', 1):
            vote = '+1'
        self.table.append({testname: [vote, timer, text]})


class TestTable(DisplayTable):
    """ test results table """
    def __init__(self):
        DisplayTable.__init__(self)

class FooterTable(DisplayTable):
    """ bottom of the report """
    def __init__(self):
        DisplayTable.__init__(self)
