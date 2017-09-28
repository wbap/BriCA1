# -*- coding: utf-8 -*-

"""
scheduler.py
=====

This module contains the `Scheduler` class which is a base class for various
types of schedulers. The `VirtualTimeSyncScheduler` is implemneted for now.

"""

__all__ = ["Scheduler", "VirtualTimeSyncScheduler", "VirtualTimeScheduler",
           "RealTimeSyncScheduler"]

from .utils import current_time
from .supervisor import NullSupervisor

from abc import ABCMeta, abstractmethod
import time

import queue


class Scheduler(object):
    """
    This class is an abstract class for creating `Scheduler`s. Subclasses must
    override the `step()` method to specify its implementation.
    """

    __metaclass__ = ABCMeta

    def __init__(self, agent, supervisor=NullSupervisor):
        """ Create a new `Scheduler` instance.

        Args:
          agent (Agent): An `Agent` to schedule.
          supervisor (Supervisor): A `Supervisor` to schedule.

        Returns:
          Scheduler: A new `Scheduler` instance.

        """

        super(Scheduler, self).__init__()
        self.agent = agent
        self.supervisor = supervisor(agent)
        self.num_steps = 0
        self.current_time = 0
        self.components = agent.get_all_components()

    def reset(self):
        """ Reset the `Scheduler`.

        Args:
          None.

        Returns:
          None.

        """

        self.num_steps = 0
        self.current_time = 0
        self.components = []

    def update(self):
        """ Update the `Scheduler` for given cognitive architecture (agent)

        Args:
          agent (Agent): a target to update.

        Returns:
          None.

        """

        self.components = self.agent.get_all_components()

    @abstractmethod
    def step(self):
        """ Step over a single iteration

        Args:
          None.

        Returns:
          int: the current time of the `Scheduler`.

        """

        pass


class VirtualTimeSyncScheduler(Scheduler):
    """
    `VirtualTimeSyncScheduler` is a `Scheduler` implementation for virutal time
    in a synced manner.
    """

    def __init__(self, agent, supervisor=NullSupervisor, interval=1):
        """ Create a new `VirtualTimeSyncScheduler` Instance.

        Args:
          interval (int): interval in milliseconds between each step

        Returns:
          VirtualTimeSyncScheduler: A new `VirtualTimeSyncScheduler` instance.

        """

        super(VirtualTimeSyncScheduler, self).__init__(
            agent,
            supervisor=NullSupervisor,
        )
        self.interval = interval

    def step(self):
        """ Step by the internal interval.

        The methods `input()`, `fire()`, and `output()` are synchronously
        called and the time is incremented by the given interval for each
        step.

        Args:
          None.

        Returns:
          int: the current time of the `Scheduler`.

        """

        for component in self.components:
            component.input(self.current_time)

        self.supervisor.step()

        for component in self.components:
            component.train()
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

        def __init__(self, time, component, action='fire'):
            """ Create a new `Event` instance.

            Args:
              time (int): the time of the `Event`.
              component (Component): `Component` to be handled.

            Returns:
              Component: a new `Component` instance.

            """

            super(VirtualTimeScheduler.Event, self).__init__()
            self.time = time
            self.component = component
            self.action = action

        def __lt__(self, other):
            return self.time < other.time

    def __init__(self, agent, supervisor=NullSupervisor):
        """ Create a new `Event` instance.

        Args:
          time (int): the time of the `Event`.
          component (Component): `Component` to be handled.

        Returns:
          Component: a new `Component` instance.

        """

        super(VirtualTimeScheduler, self).__init__(
            agent,
            supervisor=NullSupervisor,
        )
        self.event_queue = queue.PriorityQueue()

    def update(self):
        """ Update the `Scheduler` for given cognitive architecture (agent)

        Args:
          agent (Agent): a target to update.

        Returns:
          None.

        """

        super(VirtualTimeScheduler, self).update()
        for component in self.components:
            self.event_queue.put(
                VirtualTimeScheduler.Event(
                    component.offset,
                    component,
                    'sleep',
                )
            )

    def step_for_time(self, time):
        fires = []
        sleeps = []

        while not self.event_queue.empty():
            if self.event_queue.queue[0].time == time:
                event = self.event_queue.get()
                component = event.component

                if event.action == 'fire':
                    next_event = VirtualTimeScheduler.Event(
                        event.time + component.sleep,
                        component,
                        'sleep'
                    )
                    sleeps.append(component)
                else:
                    next_event = VirtualTimeScheduler.Event(
                        event.time + component.interval,
                        component,
                        'fire'
                    )
                    fires.append(component)

                self.event_queue.put(next_event)
            else:
                break

        
        for component in sleeps:
            component.output(time)

        for component in fires:
            component.input(time)

        self.supervisor.step()

        for component in fires:
            component.train()
            component.fire()

    def step(self, interval=0):
        """ Step with given interval or to the next event

        An event is dequeued and `output()`, `input()`, and `fire()` are called
        for the `Component` of interest.

        Args:
          interval (int): interval in milliseconds between each step

        Returns:
          int: the current time of the `Scheduler`.

        """

        if interval == 0:
            self.current_time = self.event_queue.queue[0].time
            self.step_for_time(self.current_time)
        else:
            self.current_time += interval
            while self.event_queue.queue[0].time <= self.current_time:
                self.step_for_time(self.event_queue.queue[0].time)

        return self.current_time


class RealTimeSyncScheduler(Scheduler):
    """
    `RealTimeSyncScheduler` is a `Scheduler` implementation for real time
    in a synced manner.
    """

    def __init__(self, agent, supervisor=NullSupervisor, interval=1):
        """ Create a new `RealTimeSyncScheduler` Instance.

        Args:
          interval (int): minimu interval in seconds between input and output
          of the modules.

        Returns:
          RealTimeSyncScheduler: A new `RealTimeSyncScheduler` instance.

        """

        self.last_input_time = -1
        self.last_output_time = -1
        self.last_spent = -1
        self.last_dt = -1

        super(RealTimeSyncScheduler, self).__init__(
            agent,
            supervisor=NullSupervisor,
        )
        self.set_interval(interval)

    def reset(self):
        super(RealTimeSyncScheduler, self).reset()
        self.set_interval(1)

    def set_interval(self, interval):
        self.interval = int(interval)
        assert self.interval > 0

    def step(self):
        """ Step by the internal interval.

        The methods `input()`, `fire()`, and `output()` are synchronously
        called for all components.

        The time when it started calling input() and output() of the
        components is stored in self.last_input_time and
        self.last_output_time, respectively.

        self.interval sets the *minimum* interval between the point in
        time when input() is called and when output() is called.
        The actual interval between input() and output() will
        always be longer than self.interval, although the scheduler
        tries to make the discrepancy minimum.

        When calling fire() of the components takes longer than the
        set interval, calling output() of the components will be
        later than the scheduled time self.input_time + self.interval.
        In this case, self.lagged will be set True.

        During the execution of this method, it will also set self.last_spent,
        which will be the time spent until all components are fired
        after self.last_input_time is set.

        Args:
          None.

        Returns:
          int: the current time of the `Scheduler`.

        """

        self.last_input_time = current_time()
        self.current_time = self.last_input_time

        for component in self.components:
            component.input(self.last_input_time)

        self.supervisor.step()

        for component in self.components:
            component.train()
            component.fire()

        self.last_spent = current_time() - self.last_input_time
        last_dt = self.interval - self.last_spent

        self.lagged = False
        if last_dt > 0:
            time.sleep(last_dt / 1000.0)
        elif last_dt < 0:
            self.lagged = True

        self.last_output_time = current_time()
        self.current_time = self.last_output_time

        for component in self.components:
            component.output(self.last_output_time)

        self.last_output_time = current_time()
        self.current_time = self.last_output_time

        return self.current_time
