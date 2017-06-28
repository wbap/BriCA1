# -*- coding: utf-8 -*-

"""
component.py
=====

This module contains the `Component`, `ConstantComponent`, `PipeComponent`, and
`NullComponent`. A `Component` is a unit of implementation which can exchange
any type of data with another `Component`. `Component`s together with `Unit`s
are collectively reffered to as `Unit`s.

"""

__all__ = ["Component", "ComponentSet", "ConstantComponent", "PipeComponent",
           "NullComponent"]

from abc import ABCMeta, abstractmethod
from copy import deepcopy

# BriCA imports
from unit import Unit


class Component(Unit):
    """
    `Component` is an abstract class for implementation units. Subclasses must
    override the `fire()` method to specify its implementation. See the sample
    implementations, `ConstantComponent`, `NullComponent`, and `PipeComponent`
    for reference.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """ Create a new `Component` instance.

        Args:
          None.

        Returns:
          Component: a new `Component` instance.

        """

        super(Component, self).__init__()
        self.last_input_time = 0
        self.last_output_time = 0
        self.offset = 0
        self.interval = 1000
        self.inputs = {}
        self.states = {}
        self.results = {}

    @abstractmethod
    def fire(self):
        """ Perform a calculation.

        Users must override `fire(self)` method to define a new sub-class of
        `Component`. `fire(self)` method implements a function of the form

          results, states <- fire(in_ports, states)

        which states that this method should be a mutator of these two member
        variables (`results` and `states`), and the result of the computation
        should solely depend on the values stored in (`in_ports` and `states`).
        One important note here is that it shall mutate results member variable
        and not `out_ports`. Values stored in `results` will automatically be
        copied to `out_ports` by the scheduler which calls `update_output()`
        method of this Module, so these must be visible and accessible from
        other Modules. This procedure is especially necessary in concurrent
        execution of multiple Modules to avoid contention.

        Args:
          None.

        Returns:
          None.

        """

        pass

    def train(self):
        """ Perform a training iteration

        Returns:
          None.

        """

        pass

    def set_state(self, id, value):
        """ Set a state value for the given ID.

        Args:
          id (str): a string ID.
          v (any): a state value to set.

        Returns:
          None.

        """

        self.states[id] = deepcopy(value)

    def get_state(self, id):
        """ Get a state value for the given ID.

        Args:
          id (str): a string ID.

        Returns:
          any: a state value for the given ID.

        """

        return self.states[id]

    def clear_state(self, id):
        """ Clear a state value for the given ID.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.states[id]

    def set_result(self, id, value):
        """ Set a result value for the given ID.

        Args:
          id (str): a string ID.
          v (any): a result value to set.

        Returns:
          None.

        """

        self.results[id] = deepcopy(value)

    def get_result(self, id):
        """ Get a result value for the given ID.

        Args:
          id (str): a string ID.

        Returns:
          any: a result value for the given ID.

        """

        return self.results[id]

    def clear_result(self, id):
        """ Clear a state value for the given ID.

        Args:
          id (str): a string ID.

        Returns:
          None.

        """

        del self.results[id]

    def input(self, time):
        """ Obtain inputs from outputs of other Modules.

        This method collects the outputs of connected modules and sets the
        values to the in-ports. It is usually called by the scheduler.

        Args:
          time (int): the scheduler's current time.

        Returns:
          None.

        """

        for id, in_port in self.in_ports.items():
            in_port.sync()
            in_port.invoke_callbacks()
            self.inputs[id] = deepcopy(in_port.buffer)

        assert self.last_input_time <= time, ("collect_input() captured a time"
                                              " travel")
        self.last_input_time = time

    def output(self, time):
        """ Expose results to `out_ports`

        This method exposes the computation results from `results` to
        `out_ports`. It is usually called by the scheduler.

        Args:
          time (int): the scheduler's current time.

        Returns:
          None.

        """

        for id, out_port in self.out_ports.items():
            if id in self.results:
                out_port.buffer = self.results[id]
                out_port.invoke_callbacks()

        assert self.last_output_time <= time, ("update_output() captured a"
                                               " time travel")
        self.last_output_time = time

    def reset(self):
        """ Reset the component state

        This method resets the internal time of the component for reuse.

        Args:
          None.

        Returns:
          None.

        """

        self.last_input_time = 0
        self.last_output_time = 0
        self.offset = 0
        self.interval = 1000


class ComponentSet(Component):
    """
    `ComponentSet` groups components to fire sequentially
    """
    def __init__(self):
        """ Create a new `ComponentSet` instance.

        Args:
          None.

        Returns:
          ComponentSet: a new `ComponentSet` instance.

        """

        super(ComponentSet, self).__init__()
        self.components = {}
        self.priorities = {}

    def add_component(self, id, component, priority):
        """ Add a `Component` for given ID and priority

        Args:
          id (str): a string ID.
          component (Component): a component to add for `id`.
          priority (int): a priority value for scheduling.

        Returns:
          None.

        """

        self.components[id] = component
        self.priorities[id] = priority

    def get_component(self, id):
        """ Get a `Component` for given ID.

        Args:
          id (str): a string ID.

        Returns:
          Component: a `Component` corresponding to the ID.

        """

        return self.components[id]

    def fire(self):
        """ Fire sub-components based on priority

        Args:
          None.

        Returns:
          None.

        """

        order = sorted(self.priorities.keys(),
                       key=lambda id: self.priorities[id])
        for id in order:
            component = self.components[id]
            component.input(self.last_input_time)
            component.fire()
            component.output(self.last_output_time)


class ConstantComponent(Component):
    """
    `ConstantComponent` copies states to out ports.

    Use `set_state` to define the output of this Module.
    """
    def __init__(self):
        """ Create a new `ConstantComponent` instance.

        Args:
          None.

        Returns:
          ConstantComponent: a new `ConstantComponent` instance.

        """

        super(ConstantComponent, self).__init__()

    def fire(self):
        """ Copy state contents to results.

        Args:
          None.

        Returns:
          None.

        """

        for id in self.states.keys():
            self.results[id] = self.states[id]


class PipeComponent(Component):
    """
    `PipeComponent` copies contents of in ports to out ports.
    """

    def __init__(self):
        """ Create a new `PipeComponent` instance.

        Args:
          None.

        Returns:
          PipeComponent: A new `PipeComponent` instance.

        """

        super(PipeComponent, self).__init__()
        self.map = []

    def set_map(self, in_id, out_id):
        """ Map from in-port to out port.

        Args:
          in_id (str): port id to map from.
          out_id (str): port id to map to.

        Returns:
          None.

        """

        self.map.append((in_id, out_id))

    def fire(self):
        for in_id, out_id in self.map:
            self.results[out_id] = self.inputs[in_id]


class NullComponent(Component):
    """
    `NullComponent` does nothing.
    """

    def __init__(self):
        """ Create a new `NullComponent` instance.

        Args:
          None.

        Returns:
          NullComponent: A new `NullComponent` instance.

        """

        super(NullComponent, self).__init__()

    def fire(self):
        """ Do nothing. Just return.

        Args:
          None.

        Returns:
          None.

        """
        pass
