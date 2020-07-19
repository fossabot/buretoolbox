#!/usr/bin/env python3

""" Utilities """

import os

def relative_path(path=None, start=None):
    """ calculate a relative path """
    if not path:
        return (None, False)

    if not start:
        start = "basedir"
    testpath = os.path.relpath(path, start)

    if testpath[0] == '.':
        return (testpath, False)
    return (testpath, True)
