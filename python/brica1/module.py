# -*- coding: utf-8 -*-

"""
module.py
=====

This module contains the class `Module` and `CognitiveArchitecture` which serve
as abstractions for distict areas in the brain or sub-regions of those areas.
`Module`s together with `Component`s are collectively reffered to as `Unit`s.

"""

__all__ = ["Module", "CognitiveArchitecture"]

import copy
import numpy

# BriCA imports
from unit import *

class Module(Unit):
    """
    A `Module` may not have an implementation and may only exchange
    `numpy.ndarray` of the type `numpy.short` through in/out ports with another
    module.
    """

    def __init__(self):
        """ Create a new `Module` instance.

        Args:
          None.

         Returns:
           Module: a new `Module` instance.

        """

        super(Module, self).__init__()
        self.components = {}
        self.submodules = {}

    def add_submodule(self, id, submodule):
        """ Add a `Module` to this `Module`.

        Args:
          id (str): a string ID.
          submodule (Module): a module to add for `id`.

        Returns:
          None.

        """

        if id in self.components:
            raise LookupError("There is already a component of the same name")
            return

        self.submodules[id] = submodule

    def get_submodule(self, id):
        """ Get a `Module` for a given `id`.

        Args:
          id (str): a string ID.

        Returns:
          Module: a module for the given `id`.

        """

        list = id.split(".")
        head = list.pop(0)
        child = self.submodules[head]

        if len(list) == 0:
            return child

        return child.get_submodule(".".join(list))

    def get_all_submodules(self):
        """ Get all `Module`s recursively.

        Args:
          None.

        Returns:
          list: a list of all `Module`s.

        """

        list = self.submodules.values()

        for submodule in list:
            list.extend(submodule.get_all_submodules())

        return list

    def remove_submodule(self, id):
        """ Remove a module from this `Module`.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.submodules[id]

    def add_component(self, id, component):
        """ Add a `Component` to this `Module`.

        Args:
          id (str): a string ID.
          component (Component): a component to add for `id`.

        Returns:
          None.

        """

        if id in self.submodules:
            raise LookupError("There is already a submodule of the same name")
            return

        self.components[id] = component

    def get_component(self, id):
        """ Get a `Component` for a given `id`.

        Args:
          id (str): a string ID.

        Returns:
          Component: a component for the given `id`.

        """

        return self.components[id]

    def get_all_components(self):
        """ Get all `Component`s of all `Module`s.

        Args:
          None.

        Returns:
          list: a list of all `Component`s.

        """

        list = self.components.values()

        for submodule in self.get_all_submodules():
            list.extend(submodule.get_all_components())

        return list

    def remove_component(self, id):
        """ Remove a component from this `Module`.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.components[id]

class CognitiveArchitecture(Module):
    """
    A `CognitiveArchitecture` is a `Module` which serves as a top-level
    container for functional `Module`s.
    """

    def __init__(self, scheduler):
        """ Create a new `CognitiveArchitecture` instance.

        Args:
          scheduler (Scheduler): a scheduler to schedule `Component` firing.

        Returns:
          CognitiveArchitecture: a new `CognitiveArchitecture` instance.

        """
        super(CognitiveArchitecture, self).__init__()
        self.scheduler = scheduler

    def step(self):
        """  Step the `Scheduler`.

        Args:
          None.

        Returns:
          None.

        """

        self.scheduler.step()

    def update_scheduler(self):
        """ Udpate the `Scheduler` with this `CognitiveArchitecture`.

        Args:
          None.

        Returns:
          None.

        """

        self.scheduler.update(self)

    def add_submodule(self, id, submodule):
        """ add a `Module` and update the `Scheduler`.

        Args:
          id (str): a string ID.
          submodule (Module): a module to add for `id`.

        Returns:
          None.

        """

        super(CognitiveArchitecture, self).add_submodule(id, submodule)
        self.update_scheduler()
