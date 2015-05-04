# -*- coding: utf-8 -*-

"""
unit.py
=====

This module contains the `Unit` modules which serves as a base class for the
`Component` and `Module` classes.

"""

__all__ = ["Unit"]

import copy
import numpy

# BriCA imports
from port import *

class Unit(object):
    """
    `Unit` is a base class for `Module`s and `Component`s with functionalities
    for handling ports.
    """

    def __init__(self):
        """ Create a new `Unit` instance.

        Args:
          None.

        Returns:
          Unit: a new `Unit` instance.

        """

        super(Unit, self).__init__()
        self.in_ports = {}
        self.out_ports = {}

    def make_in_port(self, id, length):
        """ Make an in-port of this `Unit`.

        Args:
          id (str): a string ID.
          length (int): an initial length of the value vector.

        Returns:
          None.

        """

        self.in_ports[id] = Port(numpy.zeros(length, dtype=numpy.short))

    def get_in_port(self, id):
        """ Get values in an in-port from this `Unit`.

        Args:
          id (str): a string ID.

        Returns:
          numpy.ndarray: a value vector for the in-port ID.

        """

        return self.in_ports[id]

    def remove_in_port(self, id):
        """ Remove an in-port from this `Unit`.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.in_ports[id]

    def make_out_port(self, id, length):
        """ Make an out-port of this `Unit`.

        Args:
          id (str): a string ID.
          length (int): an initial length of the value vector.

        Returns:
          None.

        """

        self.out_ports[id] = Port(numpy.zeros(length, dtype=numpy.short))

    def get_out_port(self, id):
        """ Get values in an out-port from this `Unit`.

        Args:
          id (str): a string ID.

        Returns:
          numpy.ndarray: a value vector for the in-port ID.

        """

        return self.out_ports[id]

    def remove_out_port(self, id):
        """ Remove an out-port from this `Unit`.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.out_ports[id]

    def mirror_in_port(self, target, from_id, to_id):
        """ Mirror an in-port from a target `Unit` to this `Unit`.

        Args:
          target (Unit): a `Unit` to mirror to.
          from_id (str): a port ID to mirror from.
          to_id (str): a port ID to mirror to.

        Returns:
          None.

        """

        self.get_in_port(to_id).connect(target.get_in_port(from_id))

    def mirror_out_port(self, target, from_id, to_id):
        """ Mirror an out-port from a target `Unit` to this `Unit`.

        Args:
          target (Unit): a `Unit` to mirror to.
          from_id (str): a port ID to mirror from.
          to_id (str): a port ID to mirror to.

        Returns:
          None.

        """

        target.get_out_port(from_id).connect(self.get_out_port(to_id))

    def connect(self, target, from_id, to_id):
        """ Connect an out-port of another `Unit` to an in-port.

        Args:
          target (Unit): a `Unit` to connect to.
          from_id (str): an out-port of the target `Unit`.
          to_id(str): an in-port of this `Unit`.

        Returns:
          None.

        """

        self.get_in_port(to_id).connect(target.get_out_port(from_id))
