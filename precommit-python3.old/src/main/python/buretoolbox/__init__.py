#!/usr/bin/env python3

"""basic routines for all of buretoolbox """

import argparse
import base64
import datetime
import difflib
import filecmp
import getpass
import http.client
import importlib
import json
import logging
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import types
import urllib.error
import urllib.request
import urllib.parse

from pprint import pprint
from time import gmtime, strftime, sleep

sys.dont_write_bytecode = True


CHANGED_FILES = []
CHANGED_MODULES = []
CHANGED_PARENT_MODULE = []

OSTYPE = os.uname()[0]
PATCH_OR_ISSUE = ''
PATCHDATA = None
PATCHSYSTEM = None

PERSONALITY = None

NEEDED_TESTS = {}

VERSION_DISPLAY = False

GLOBALTIMER = None
RUNMODE = 'patch'

FAILRUN = False

