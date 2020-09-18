#!/usr/bin/env python3

""" cooridnator object to link everything together """

import config
import pluginhandler

class Coordinator():
  """ coordinator object to link everything together """

  def __init__(self):
    self.pluginhandler = pluginhandler.PluginHandler(plugin_package='buretoolbox')
    self.config = config.Config()