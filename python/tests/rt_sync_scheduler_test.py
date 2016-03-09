#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import unittest
import numpy
import brica1

# scheduler time accuracy tolerance in seconds
TOLERANCE = 1e-3


class TimeReporterComponent(brica1.Component):

    def __init__(self, delay=0):
        super(TimeReporterComponent, self).__init__()
        self.delay = delay

    def fire(self):

        time.sleep(self.delay)
        self.results['fire_time'] = numpy.array([time.time(),])


class RealTimeSyncSchedulerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        ca = brica1.Agent()
        s = brica1.RealTimeSyncScheduler(ca)

        c =TimeReporterComponent()

        CompSet = brica1.ComponentSet()
        CompSet.add_component("C", c, 0)

        ModA = brica1.Module()
        ModA.add_component("CompSet", CompSet)

        ca.add_submodule("ModA", ModA)

        s.set_interval(0.1)

        s.step()
        for _ in range(5):
            scheduled_time = s.current_time + s.interval
            s.step()
            self.assertGreater(s.current_time, scheduled_time)
            self.assertLessEqual(abs(s.current_time - scheduled_time), 
                                 TOLERANCE)
            self.assertFalse(s.lagged)


    def test_lagging(self):
        ca = brica1.Agent()
        s = brica1.RealTimeSyncScheduler(ca)

        c =TimeReporterComponent()

        CompSet = brica1.ComponentSet()
        CompSet.add_component("C", c, 0)

        ModA = brica1.Module()
        ModA.add_component("CompSet", CompSet)

        ca.add_submodule("ModA", ModA)

        s.set_interval(0.1)
        c.delay = 0

        s.step()
        scheduled_time = s.current_time + s.interval
        s.step()
        self.assertGreater(s.current_time, scheduled_time)
        self.assertLessEqual(abs(s.current_time - scheduled_time), 
                             TOLERANCE)
        self.assertFalse(s.lagged)
        
        c_interval = 0.2
        c.delay = c_interval
        s.step()
        self.assertTrue(s.lagged)




if __name__ == '__main__':
    test_classes = [RealTimeSyncSchedulerTest, ]

    suites_list = []

    loader = unittest.TestLoader()

    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    all_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(all_suite)
