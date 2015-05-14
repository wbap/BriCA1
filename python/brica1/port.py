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
        """ Create a new `Port` instance.

        Args:
          None.

        Returns:
          Scheduler: A new `Port` instance.

        """

        super(Port, self).__init__()
        self.buffer = value

    def connect(self, target):
        """ Create a connection to the target `Port`.

        Args:
          target (Port): a `Port` to connect to.

        Returns:
          None.

        """

        self.connection = Connection(target, self)

    def sync(self):
        """ Sync self with the `Connection`.

        Args:
          None.

        Returns:
          None.

        """

        if hasattr(self, 'connection'):
            self.connection.sync()
