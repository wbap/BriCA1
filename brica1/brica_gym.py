# -*- coding: utf-8 -*-

"""
gym.py
=====

This module contains the class `GymAgent` which acts as a wrapper for the
OpenAI Gym library. The `Agent` forwards information given from the environment
to the respective `Port`s inside the `GymAgent`.

"""

import numpy as np

from brica1 import Component
from brica1 import Module, Agent
from brica1 import alias_in_port, alias_out_port, connect

__all__ = ['EnvComponent', 'GymAgent']


class EnvComponent(Component):
    def __init__(self, env):
        super(EnvComponent, self).__init__()

        self.env = env

        self.make_in_port('action', 1)
        self.make_in_port('token_in', 1)
        self.make_out_port('observation', 1)
        self.make_out_port('reward', 1)
        self.make_out_port('done', 1)
        self.make_out_port('token_out', 1)
        self.done = 0
        self.info = None
        self.cnt = 0
        self.flush = False

        observation = env.reset()
        self.results['observation'] = observation
        self.results['token_out'] = np.array([self.cnt])

    def fire(self):
        if self.flush:
            return
        if self.inputs['token_in'][0]==self.cnt:
            action = self.inputs['action'][0]
            observation, reward, done, info = self.env.step(action)
            self.info = info
            self.cnt += 1
            # print("Gym:", self.cnt, observation, reward, done, action)
            self.results['token_in'] = self.inputs['token_in']
            if done:
                self.done = 1
            else:
                self.done = 0
            self.results['observation'] = observation
            self.results['reward'] = np.array([reward])
            self.results['done'] = np.array([self.done])
            self.results['token_out'] = np.array([self.cnt])
        else:
             self.results['token_out'] = self.inputs['token_in']

    def reset(self):
        self.cnt = 0
        self.flush = False
        self.results['observation'] = self.env.reset()
        self.results['token_out'] = np.array([self.cnt])
        self.inputs['token_in'] = np.array([self.cnt])

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
        self.make_in_port('token_in', 1)
        self.make_out_port('action', 1)
        self.make_out_port('token_out', 1)

        alias_in_port((model, 'observation'), (self, 'observation'))
        alias_in_port((model, 'reward'), (self, 'reward'))
        alias_in_port((model, 'done'), (self, 'done'))
        alias_in_port((model, 'token_in'), (self, 'token_in'))
        alias_out_port((model, 'action'), (self, 'action'))
        alias_out_port((model, 'token_out'), (self, 'token_out'))

        connect((self.env, 'observation'), (self, 'observation'))
        connect((self.env, 'reward'), (self, 'reward'))
        connect((self.env, 'done'), (self, 'done'))
        connect((self.env, 'token_out'), (self, 'token_in'))
        connect((self, 'action'), (self.env, 'action'))
        connect((self, 'token_out'), (self.env, 'token_in'))
