#!/usr/bin/env python3

""" Utilities """

import logging
import os
import subprocess
import tempfile

import pytest

def relative_path(path=None, start=None, config=None):
    """ calculate a relative path """
    if not path:
        return (None, False)

    if not start:
        start = config.get('basedir')
    testpath = os.path.relpath(path, start)

    if testpath[0] == '.':
        return (testpath, False)
    return (testpath, True)

def test_relative_path():
  (path, truthy) = relative_path(config={'basedir':'/'},path='/tmp')
  assert(path in 'tmp')
  assert(truthy)

  (path, truthy) = relative_path(config={'basedir':'/usr'},path='/tmp', start='/bin')
  assert(not truthy)

  (path, truthy) = relative_path(config={'basedir':'/'},path='/usr/bin', start='/usr')
  assert(path in 'bin')
  assert(truthy)


def print_and_redirect(args=None, logfilename=None):
  """ Execute a command, sending output to a file and the screen """

  returncode = 0

  if logfilename:
    logfile = open(logfilename, "wb+")
  else:
    logfile = tempfile.NamedTemporaryFile()

  try:
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
      print(line.decode('utf-8'))
      logfile.write(line)
    logfile.close()
    returncode = process.returncode
  except FileNotFoundError as err:
    logging.error("%s failed with %s", ' '.join(args), err)
    returncode = -1
  return returncode


def test_print_and_redirect1(capsys):
  print_and_redirect(['echo', '1', '2', '3'])
  stdout = capsys.readouterr()
  assert(stdout.out == '1 2 3\n\n')

def test_print_and_redirect2(tmpdir):
  filename = tmpdir.mkdir('test').join('test.txt')
  print_and_redirect(['echo', '1', '2', '3'], filename)
  assert(filename.read() == '1 2 3\n')
