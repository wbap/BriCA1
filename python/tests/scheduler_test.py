#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import unittest
import numpy
import brica1

class VirtualTimeSyncSchedulerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_component(self):
        s = brica1.VirtualTimeSyncScheduler(1.0)
        ca = brica1.CognitiveArchitecture(s)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        ca.add_submodule("ModA", ModA)

        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.connect(CompA, "out", "in")
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        CompC.connect(CompB, "out", "in")

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA.set_state("out", v)

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())

    def test_module(self):
        s = brica1.VirtualTimeSyncScheduler(1.0)
        ca = brica1.CognitiveArchitecture(s)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        ModA = brica1.Module()
        ModB = brica1.Module()
        ModC = brica1.Module()

        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)

        ModA.make_out_port("out", 3)
        ModB.make_in_port("in", 3)
        ModB.make_out_port("out", 3)
        ModC.make_in_port("in", 3)

        ModA.add_component("CompA", CompA)
        ModB.add_component("CompB", CompB)
        ModC.add_component("CompC", CompC)

        CompA.mirror_out_port(ModA, "out", "out")
        CompB.mirror_in_port(ModB, "in", "in")
        CompB.mirror_out_port(ModB, "out", "out")
        CompC.mirror_in_port(ModC, "in", "in")

        ModB.connect(ModA, "out", "in")
        ModC.connect(ModB, "out", "in")

        ca.add_submodule("ModA", ModA)
        ca.add_submodule("ModB", ModB)
        ca.add_submodule("ModC", ModC)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA.set_state("out", v)

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())

if __name__ == '__main__':

    test_classes = [VirtualTimeSyncSchedulerTest]

    suites_list = []

    loader = unittest.TestLoader()

    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    all_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(all_suite)
