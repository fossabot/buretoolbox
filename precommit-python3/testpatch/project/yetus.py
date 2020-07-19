#!/usr/bin/env python3

"""  default project """

from . import ProjectPlugin
from ..build.maven import Maven

class Yetus(ProjectPlugin, Maven):
    """ default project """

    def __init__(self):
        Maven.__init__(self)
        ProjectPlugin.__init__(self)
        self.name = 'yetus'
        self.buildtool = 'maven'
        self.jira_re = '^YETUS-[0-9]+$'
        self.github_repo = "apache/yetus"
        self.default_branch = 'main'

    def module_params(self, repostatus=None, testname=None):
        if 'mvninstall' in testname:
            if 'branch' in repostatus:
                return
