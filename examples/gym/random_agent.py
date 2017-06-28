#!/usr/bin/env python

import gym
import logging
import numpy as np

import brica1

print brica1.__file__

import brica1.gym

class RandomComponent(brica1.Component):
    def __init__(self, action_space):
        super(RandomComponent, self).__init__()
        self.action_space = action_space

        self.make_in_port('observation', 1)
        self.make_in_port('reward', 1)
        self.make_in_port('done', 1)
        self.make_in_port('info', 1)
        self.make_out_port('action', 1)

        init = self.action_space.sample()

        self.get_out_port('action').buffer = init
        self.results['action'] = init

    def fire(self):
        self.results['action'] = np.array([self.action_space.sample()])

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    env = gym.make('CartPole-v0')

    outdir = '/tmp/random-agent-results'
    env.monitor.start(outdir, force=True, seed=0)

    random = RandomComponent(env.action_space)

    agent = brica1.gym.GymAgent(random, env)
    scheduler = brica1.VirtualTimeSyncScheduler(agent)

    episode_count = 100
    max_steps = 200
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()

        for j in range(max_steps):
            scheduler.step()

    # Dump result info to disk
    env.monitor.close()
