# -*- coding: utf-8 -*-

"""
gym.py
=====

This module contains the class `GymAgent` which acts as a wrapper for the
OpenAI Gym library. The `Agent` forwards information given from the environment
to the respective `Port`s inside the `GymAgent`.

"""

import numpy as np

import brica1

__all__ = ['EnvComponent', 'GymAgent']


class EnvComponent(brica1.Component):
    def __init__(self, env, obs_dim, action_dim):
        super(EnvComponent, self).__init__()

        self.env = env

        self.make_in_port('action', action_dim)
        self.make_in_port('token_in', 1)
        self.make_out_port('observation', obs_dim)
        self.make_out_port('reward', 1)
        self.make_out_port('done', 1)
        self.make_out_port('token_out', 1)
        self.done = 0
        self.info = None
        self.cnt = 0
        self.flush = False
        self.action_dim = action_dim

        observation = env.reset()
        self.results['observation'] = observation
        self.results['token_out'] = np.array([self.cnt])
        self.results['done'] = np.array([0])
        self.results['reward'] = np.array([0.0])

    def fire(self):
        if self.flush:
            return
        if self.inputs['token_in'][0] == self.cnt:
            if self.cnt != 0:
                if self.action_dim == 1:
                    if self.inputs['action'].size == 1:
                        action = self.inputs['action'][0]
                    else:   # one-hot vector to int
                        if self.inputs['action'].max() == 0.0:
                            action = 0
                        else:
                            action = np.argmax(self.inputs['action']) + 1
                else:
                    action = self.inputs['action']
                observation, reward, done, info = self.env.step(action)
                self.info = info
                self.results['observation'] = observation
                self.results['reward'] = np.array([reward])
                if done:
                    self.done = 1
                else:
                    self.done = 0
                self.results['done'] = np.array([self.done])
            self.cnt += 1
        self.results['token_out'] = np.array([self.cnt])

    def reset(self):
        self.cnt = 0
        self.flush = False
        self.done = False
        self.results['observation'] = self.env.reset()
        self.results['done'] = np.array([0])
        self.results['reward'] = np.array([0.0])
        self.results['token_out'] = np.array([0])
        self.inputs['token_in'] = np.array([0])

class GymAgent(brica1.Agent):
    def __init__(self, model, env, obs_dim, action_dim):
        super(GymAgent, self).__init__()

        self.env = EnvComponent(env, obs_dim, action_dim)
        self.add_component('env', self.env)

        if isinstance(model, brica1.Component):
            self.add_component('model', model)
        if isinstance(model, brica1.Module):
            self.add_submodule('model', model)

        self.make_in_port('observation', obs_dim)
        self.make_in_port('reward', 1)
        self.make_in_port('done', 1)
        self.make_in_port('token_in', 1)
        self.make_out_port('action', action_dim)
        self.make_out_port('token_out', 1)

        brica1.utils.alias_in_port((model, 'observation'), (self, 'observation'))
        brica1.utils.alias_in_port((model, 'reward'), (self, 'reward'))
        brica1.utils.alias_in_port((model, 'done'), (self, 'done'))
        brica1.utils.alias_in_port((model, 'token_in'), (self, 'token_in'))
        brica1.utils.alias_out_port((model, 'action'), (self, 'action'))
        brica1.utils.alias_out_port((model, 'token_out'), (self, 'token_out'))

        brica1.utils.connect((self.env, 'observation'), (self, 'observation'))
        brica1.utils.connect((self.env, 'reward'), (self, 'reward'))
        brica1.utils.connect((self.env, 'done'), (self, 'done'))
        brica1.utils.connect((self.env, 'token_out'), (self, 'token_in'))
        brica1.utils.connect((self, 'action'), (self.env, 'action'))
        brica1.utils.connect((self, 'token_out'), (self.env, 'token_in'))


class ComponentCaller(type):
    def __new__(mcs, name, base, attr):
        # suppress Component.fire()
        if name != "Component":
            # fire() gets decorated.
            attr["fire"] = mcs.decorate(attr["fire"])
        return super().__new__(mcs, name, base, attr)

    @classmethod
    def decorate(mcs, fire):
        def new_fire(self):
            if self.inputs['token_in'][0] == self.token + 1:
                self.token = self.inputs['token_in'][0]
                fire(self)
            self.results['token_out'] = self.inputs['token_in']
        return new_fire


class Component(brica1.Component, metaclass=ComponentCaller):
    def __init__(self):
        super(Component, self).__init__()
        self.token = 0
        self.make_in_port('token_in', 1)
        self.make_out_port('token_out', 1)

    def fire(self):
        pass

