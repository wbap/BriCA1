# -*- coding: utf-8 -*-

"""
port.py
=====

This module contains the class `Port`.

"""

# BriCA imports
from .connection import Connection


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
        self.callbacks = []

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

    def register_callback(self, f):
        """ Register a callback function to this `Port`

        Args:
          f (Function): a function to register

        Returns:
          None.

        """

        self.callbacks.append(f)

    def invoke_callbacks(self):
        """ Invoke all callback functions with buffer value as argument

        Args:
          None.

        Returns:
          None.

        """

        for f in self.callbacks:
            f(self.buffer)
