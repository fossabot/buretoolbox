#!/usr/bin/env python3

""" Object to keep track of time """

import sys
import time

sys.dont_write_bytecode = True


class Timekeeper():

    """ clock object """

    def __init__(self, timer=None):
        if timer:
            self.starttime = timer
        else:
            self.starttime = time.time()

        self.stoptime = None
        self.delta = None

    def start(self):
        """ start the clock """
        self.starttime = time.time()

    def stop(self):
        """ stop the clock """
        self.stoptime = time.time()
        self.delta = self.stoptime - self.starttime

    def offset(self, offset=0):
        """ add an offset to this clock """
        self.starttime = self.starttime - offset

    def result(self):
        """ give a min + secs text string """
        mins = self.delta / 60
        secs = self.delta % 60
        return '%3dm %02ds' % (mins, secs)
