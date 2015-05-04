# -*- coding: utf-8 -*-

"""
scheduler.py
=====

This module contains the `Scheduler` class which is a base class for various
types of schedulers. The `VirtualTimeSyncScheduler` is implemneted for now.

"""

__all__ = ["Scheduler", "VirtualTimeSyncScheduler"]

from abc import ABCMeta, abstractmethod
import copy
import numpy

class Scheduler(object):
    """
    This class is an abstract class for creating schedulers. Subclasses must
    override the `step()` method to specify its implementation.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """ Create a new Scheduler instance.

        Args:
          None.

        Returns:
          Scheduler: A new Scheduler instance.

        """

        super(Scheduler, self).__init__()
        self.num_steps = 0
        self.current_time = 0.0
        self.components = []

    def reset(self):
        """ Reset the scheduler.

        Args:
          None.

        Returns:
          None.

        """

        self.num_steps = 0
        self.current_time = 0.0
        self.components = []

    def update(self, ca):
        """ Update the scheduler for given cognitive architecture (ca)

        Args:
          ca (CognitiveArchitecture): a target to update.

        Returns:
          None.

        """

        self.components = ca.get_all_components()

    @abstractmethod
    def step(self):
        """ Step over a single iteration

        Args:
          None.

        Returns:
          float: the current time of the scheduler

        """

        pass

class VirtualTimeSyncScheduler(Scheduler):
    """
    VirtualTimeSyncScheduler is a Scheduler implementation for virutal time in
    a synced manner.
    """

    def __init__(self, interval=1.0):
        """ Create a new VirtualTimeSyncScheduler Instance.

        Args:
          interval (float): interval between each step

        Returns:
          VirtualTimeSyncScheduler: A new VirtualTimeSyncScheduler instance.

        """

        super(VirtualTimeSyncScheduler, self).__init__()
        self.interval = interval

    def step(self):
        """ Step by the internal interval.

        The methods `input()`, `fire()`, and `output()` are synchronously
        called and the time is incremented by the given interval for each
        step.

        Args:
          None.

        Returns:
          float: the current time of the scheduler

        """

        for component in self.components:
            component.collect_input(self.current_time)

        for component in self.components:
            component.fire()

        self.current_time = self.current_time + self.interval

        for component in self.components:
            component.update_output(self.current_time)

        return self.current_time
