#!/usr/bin/env python3
""" Robots """

from ..build import BuildPlugin


class ProjectPlugin(BuildPlugin):
    """ Project Definition """
    def __init__(self):
        BuildPlugin.__init__(self)
        self.kind = "project"

    def set_defaults(self):
        """ override any defaults """
