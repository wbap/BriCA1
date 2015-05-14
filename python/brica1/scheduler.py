# -*- coding: utf-8 -*-

"""
scheduler.py
=====

This module contains the `Scheduler` class which is a base class for various
types of schedulers. The `VirtualTimeSyncScheduler` is implemneted for now.

"""

__all__ = ["Scheduler", "VirtualTimeSyncScheduler", "VirtualTimeScheduler"]

from abc import ABCMeta, abstractmethod
import copy
import numpy

import Queue

class Scheduler(object):
    """
    This class is an abstract class for creating `Scheduler`s. Subclasses must
    override the `step()` method to specify its implementation.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """ Create a new `Scheduler` instance.

        Args:
          None.

        Returns:
          Scheduler: A new `Scheduler` instance.

        """

        super(Scheduler, self).__init__()
        self.num_steps = 0
        self.current_time = 0.0
        self.components = []

    def reset(self):
        """ Reset the `Scheduler`.

        Args:
          None.

        Returns:
          None.

        """

        self.num_steps = 0
        self.current_time = 0.0
        self.components = []

    def update(self, ca):
        """ Update the `Scheduler` for given cognitive architecture (ca)

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
          float: the current time of the `Scheduler`.

        """

        pass

class VirtualTimeSyncScheduler(Scheduler):
    """
    `VirtualTimeSyncScheduler` is a `Scheduler` implementation for virutal time
    in a synced manner.
    """

    def __init__(self, interval=1.0):
        """ Create a new `VirtualTimeSyncScheduler` Instance.

        Args:
          interval (float): interval between each step

        Returns:
          VirtualTimeSyncScheduler: A new `VirtualTimeSyncScheduler` instance.

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
          float: the current time of the `Scheduler`.

        """

        for component in self.components:
            component.input(self.current_time)

        for component in self.components:
            component.fire()

        self.current_time = self.current_time + self.interval

        for component in self.components:
            component.output(self.current_time)

        return self.current_time

class VirtualTimeScheduler(Scheduler):
    """
    `VirtualTimeScheduler` is a `Scheduler` implementation for virutal time.
    """

    class Event(object):
        """
        `Event` is a queue object for `PriorityQueue` in VirtualTimeScheduler.
        """

        def __init__(self, time, component):
            """ Create a new `Event` instance.

            Args:
              time (float): the time of the `Event`.
              component (Component): `Component` to be handled.

            Returns:
              Component: a new `Component` instance.

            """

            super(VirtualTimeScheduler.Event, self).__init__()
            self.time = time
            self.component = component

        def __cmp__(self, other):
            return cmp(self.time, other.time)

    def __init__(self):
        """ Create a new `Event` instance.

        Args:
          time (float): the time of the `Event`.
          component (Component): `Component` to be handled.

        Returns:
          Component: a new `Component` instance.

        """

        super(VirtualTimeScheduler, self).__init__()
        self.event_queue = Queue.PriorityQueue()

    def update(self, ca):
        """ Update the `Scheduler` for given cognitive architecture (ca)

        Args:
          ca (CognitiveArchitecture): a target to update.

        Returns:
          None.

        """

        super(VirtualTimeScheduler, self).update(ca)
        for component in self.components:
            component.input(self.current_time)
            component.fire()
            self.event_queue.put(VirtualTimeScheduler.Event(component.offset + component.last_input_time + component.interval, component))

    def step(self):
        """ Step by the internal interval.

        An event is dequeued and `output()`, `input()`, and `fire()` are called
        for the `Component` of interest.

        Args:
          None.

        Returns:
          float: the current time of the `Scheduler`.

        """

        e = self.event_queue.get()
        self.current_time = e.time
        component = e.component
        component.output(self.current_time)
        component.input(self.current_time)
        component.fire()

        self.event_queue.put(VirtualTimeScheduler.Event(self.current_time + component.interval, component))

        return self.current_time
