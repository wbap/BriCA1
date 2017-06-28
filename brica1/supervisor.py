# -*- coding: utf-8 -*-

"""
supervisor.py
=====

This module contains the `Supervisor` and `NullSupervisor`. A `Supervisor`
controls the behaviour of component training.

"""

__all__ = ["Supervisor", "NullSupervisor"]

from abc import ABCMeta, abstractmethod


class Supervisor(object):
    """
    This class is an abstract class for creating `Supervisor`s. Subclasses must
    override the `step()` method to specify its implementation
    """

    __metaclass__ = ABCMeta

    def __init__(self, agent):
        """ Create a new `Supervisor` instance.

        Args:
          None.

        Returns:
          Supervisor: A new `Supervisor` instance.

        """

        super(Supervisor, self).__init__()
        self.agent = agent
        self.components = agent.get_all_components()

    @abstractmethod
    def step(self):
        pass


class NullSupervisor(Supervisor):
    """
    `NullSupervisor` is a `Supervisor` implementation which does absolutely
    nothing for each step.
    """

    def __init__(self, agent):
        """ Create a new `NullSupervisor` instance.

        Args:
          None.

        Returns:
          Supervisor: A new `NullSupervisor` instance.

        """

        super(NullSupervisor, self).__init__(agent)

    def step(self):
        """ Do nothing!

        Args:
          None.

        Returns:
          None.

        """

        pass
