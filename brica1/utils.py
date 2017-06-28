# -*- coding: utf-8 -*-

"""
utils.py
=====

This modules contains utility functions for BriCA.

"""

import time

__all__ = ["current_time", "current_time_millis", "connect", "alias_in_port",
           "alias_out_port"]


def current_time():
    return time.time()


def current_time_millis():
    return int(time.time() * 1000)


def connect(from_tuple, to_tuple):
    """ Connect ports of two units

    Args:
      from_tuple (tuple<Unit, str>):  Unit and port id to connect from.
      to_tuple (tuple<Unit, str>): Unit and port id to connect to.

    Returns:
      None.

    """

    from_unit, from_port = from_tuple
    to_unit, to_port = to_tuple

    to_unit.connect(from_unit, from_port, to_port)


def alias_in_port(from_tuple, to_tuple):
    """ Alias in-ports of two units

    Args:
      from_tuple (tuple<Unit, str>): Unit and port id to alias from.
      to_tuple (tuple<Unit, str>): Unit and port id to alias to.

    Returns:
      None.

    """

    from_unit, from_port = from_tuple
    to_unit, to_port = to_tuple

    to_unit.alias_in_port(from_unit, from_port, to_port)


def alias_out_port(from_tuple, to_tuple):
    """ Alias out-ports of two units

    Args:
      from_tuple (tuple<Unit, str>): Unit and port id to alias from.
      to_tuple (tuple<Unit, str>): Unit and port id to alias to.

    Returns:
      None.

    """

    from_unit, from_port = from_tuple
    to_unit, to_port = to_tuple

    to_unit.alias_out_port(from_unit, from_port, to_port)
