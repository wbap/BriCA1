# -*- coding: utf-8 -*-

"""
port.py
=====

This module contains the class `Port`.

"""

import copy

# BriCA imports
from connection import *

class Port(object):
    """
    A `Port` has a buffer value and a outward connection to another port.
    There may only be one outward connection but multiple inward connections.
    """

    def __init__(self, value):
        super(Port, self).__init__()
        self.buffer = value

    def connect(self, target):
        self.connection = Connection(target, self)

    def sync(self):
        if hasattr(self, 'connection'):
            self.connection.sync()
