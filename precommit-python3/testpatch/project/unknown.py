#!/usr/bin/env python3

"""  default project """

from . import ProjectPlugin

class Unknown(ProjectPlugin):
    """ default project """

    def __init__(self):
        ProjectPlugin.__init__(self)
        self.name = "unknown"
