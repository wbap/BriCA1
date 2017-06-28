# -*- coding: utf-8 -*-

"""
connection.py
=====

This module contains the class `Connection`.

"""


class Connection(object):
    """
    A `Connection` connects two `Port`s and can be `sync`ed in one direction.
    """

    def __init__(self, from_port, to_port):
        """ Create a Connection instance.

        Args:
          module (Module): module containing the `from_port_id`
          from_port_id (str): out-port id of `module`
          to_port_id (str): in-port id of target module

        Returns:
          Connection: a new Connection instance.
        """

        super(Connection, self).__init__()
        self.from_port = from_port
        self.to_port = to_port

    def sync(self):
        """ Sync the value from `from_port` to `to_port`.

        Args:
          None.

        Returns:
          None.

        """

        self.to_port.buffer = self.from_port.buffer
