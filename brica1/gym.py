# -*- coding: utf-8 -*-

"""
gym.py
=====

This module contains the class `GymAgent` which acts as a wrapper for the
OpenAI Gym library. The `Agent` forwards information given from the environment
to the respective `Port`s inside the `GymAgent`.

"""

import numpy as np

from .component import Component
from .module import Module, Agent
from .utils import alias_in_port, alias_out_port, connect

__all__ = ['EnvComponent', 'GymAgent']


class EnvComponent(Component):
    def __init__(self, env):
        super(EnvComponent, self).__init__()

        self.env = env

        self.make_in_port('action', 1)
        self.make_out_port('observation', 1)
        self.make_out_port('reward', 1)
        self.make_out_port('done', 1)
        self.make_out_port('info', 1)

        observation = env.reset()

        self.get_out_port('observation').buffer = observation
        self.results['observation'] = observation
        self.get_out_port('done').buffer = False
        self.results['done'] = False

    def fire(self):
        action = self.inputs['action'][0]
        observation, reward, done, info = self.env.step(action)
        if done:
            self.env.reset()
        self.results['observation'] = observation
        self.results['reward'] = np.array([reward])
        # self.results['done'] = done
        # self.results['info'] = info


class GymAgent(Agent):
    def __init__(self, model, env):
        super(GymAgent, self).__init__()

        self.env = EnvComponent(env)
        self.add_component('env', self.env)

        if isinstance(model, Component):
            self.add_component('model', model)
        if isinstance(model, Module):
            self.add_submodule('model', model)

        self.make_in_port('observation', 1)
        self.make_in_port('reward', 1)
        self.make_in_port('done', 1)
        self.make_in_port('info', 1)
        self.make_out_port('action', 1)

        alias_in_port((model, 'observation'), (self, 'observation'))
        alias_in_port((model, 'reward'), (self, 'reward'))
        alias_in_port((model, 'done'), (self, 'done'))
        alias_in_port((model, 'info'), (self, 'info'))
        alias_out_port((model, 'action'), (self, 'action'))

        connect((self.env, 'observation'), (self, 'observation'))
        connect((self.env, 'reward'), (self, 'reward'))
        connect((self.env, 'done'), (self, 'done'))
        connect((self.env, 'info'), (self, 'info'))
        connect((self, 'action'), (self.env, 'action'))
