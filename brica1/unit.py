# -*- coding: utf-8 -*-

"""
unit.py
=====

This module contains the `Unit` modules which serves as a base class for the
`Component` and `Module` classes.

"""

__all__ = ["Unit"]

import numpy

# BriCA imports
from .port import Port


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

    def set_in_port(self, id, port):
        """ Set a port with an actual instance.

        Args:
          id (str): a string ID.
          port (Port): a Port instance to set.

        Returns:
          None.

        """

        self.in_ports[id] = port

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

    def set_out_port(self, id, port):
        """ Set a port with an actual instance.

        Args:
          id (str): a string ID.
          port (Port): a Port instance to set.

        Returns:
          None.

        """

        self.out_ports[id] = port

    def remove_out_port(self, id):
        """ Remove an out-port from this `Unit`.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.out_ports[id]

    def alias_in_port(self, target, from_id, to_id):
        """ Alias an in-port from a target `Unit` to this `Unit`.

        Technical note: ALWAYS alias ports OUTSIDE IN

        Args:
          target (Unit): a `Unit` to alias from.
          from_id (str): a port ID to alias from.
          to_id (str): a port ID to alias to.

        Returns:
          None.

        """

        to_port = self.get_in_port(to_id)
        from_port = target.get_in_port(from_id)
        from_port.callbacks.extend(to_port.callbacks)
        self.set_in_port(to_id, from_port)

    def alias_out_port(self, target, from_id, to_id):
        """ Alias an out-port from a target `Unit` to this `Unit`.

        Technical note: ALWAYS alias ports OUTSIDE IN

        Args:
          target (Unit): a `Unit` to alias from.
          from_id (str): a port ID to alias from.
          to_id (str): a port ID to alias to.

        Returns:
          None.

        """

        self.set_out_port(to_id, target.get_out_port(from_id))

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
