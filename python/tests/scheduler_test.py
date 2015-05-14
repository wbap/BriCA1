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

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.connect(CompA, "out", "in")
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        CompC.connect(CompB, "out", "in")

        ca.add_submodule("ModA", ModA)

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

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        ModA = brica1.Module()
        ModB = brica1.Module()
        ModC = brica1.Module()
        ModD = brica1.Module()

        CompA.set_state("out", v)
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

        CompA.alias_out_port(ModA, "out", "out")
        CompB.alias_in_port(ModB, "in", "in")
        CompB.alias_out_port(ModB, "out", "out")
        CompC.alias_in_port(ModC, "in", "in")

        ModB.connect(ModA, "out", "in")
        ModC.connect(ModB, "out", "in")

        ModD.add_submodule("ModA", ModA)
        ModD.add_submodule("ModB", ModB)
        ModD.add_submodule("ModC", ModC)

        ca.add_submodule("ModD", ModD)

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
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
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
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
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

    def test_nested(self):
        s = brica1.VirtualTimeSyncScheduler(1.0)
        ca = brica1.CognitiveArchitecture(s)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        ModA = brica1.Module()
        ModB = brica1.Module()
        ModC = brica1.Module()

        SupA = brica1.Module()
        SupB = brica1.Module()
        SupC = brica1.Module()

        Top = brica1.Module()

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)

        ModA.make_out_port("out", 3)
        ModB.make_in_port("in", 3)
        ModB.make_out_port("out", 3)
        ModC.make_in_port("in", 3)

        SupA.make_out_port("out", 3)
        SupB.make_in_port("in", 3)
        SupB.make_out_port("out", 3)
        SupC.make_in_port("in", 3)

        SupA.add_submodule("ModA", ModA)
        SupB.add_submodule("ModB", ModB)
        SupC.add_submodule("ModC", ModC)

        ModA.add_component("CompA", CompA)
        ModB.add_component("CompB", CompB)
        ModC.add_component("CompC", CompC)

        # Out ports must be aliased inside-out
        CompA.alias_out_port(ModA, "out", "out")
        ModA.alias_out_port(SupA, "out", "out")

        # In ports must be aliased outside-in
        ModB.alias_in_port(SupB, "in", "in")
        CompB.alias_in_port(ModB, "in", "in")

        # Out ports must be aliased inside-out
        CompB.alias_out_port(ModB, "out", "out")
        ModB.alias_out_port(SupB, "out", "out")

        # In ports must be aliased outside-in
        ModC.alias_in_port(SupC, "in", "in")
        CompC.alias_in_port(ModC, "in", "in")

        SupB.connect(SupA, "out", "in")
        SupC.connect(SupB, "out", "in")

        Top.add_submodule("SupA", SupA)
        Top.add_submodule("SupB", SupB)
        Top.add_submodule("SupC", SupC)

        ca.add_submodule("Top", Top)

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())

        ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == v).all())

class VirtualTimeSchedulerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_component(self):
        s = brica1.VirtualTimeScheduler()
        ca = brica1.CognitiveArchitecture(s)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 2.0
        CompB.offset = 0.0
        CompC.offset = 1.0

        CompA.interval = 5.0
        CompB.interval = 5.0
        CompC.interval = 5.0

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.connect(CompA, "out", "in")
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        CompC.connect(CompB, "out", "in")

        ca.add_submodule("ModA", ModA)

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 5.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 6.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 7.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 10.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 11.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 12.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 15.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v   ).all())
        self.assertEquals(time, 16.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertEquals(time, 17.0)

    def test_module(self):
        s = brica1.VirtualTimeScheduler()
        ca = brica1.CognitiveArchitecture(s)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 2.0
        CompB.offset = 0.0
        CompC.offset = 1.0

        CompA.interval = 5.0
        CompB.interval = 5.0
        CompC.interval = 5.0

        ModA = brica1.Module()
        ModB = brica1.Module()
        ModC = brica1.Module()
        ModD = brica1.Module()

        CompA.set_state("out", v)
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

        CompA.alias_out_port(ModA, "out", "out")
        CompB.alias_in_port(ModB, "in", "in")
        CompB.alias_out_port(ModB, "out", "out")
        CompC.alias_in_port(ModC, "in", "in")

        ModB.connect(ModA, "out", "in")
        ModC.connect(ModB, "out", "in")

        ModD.add_submodule("ModA", ModA)
        ModD.add_submodule("ModB", ModB)
        ModD.add_submodule("ModC", ModC)

        ca.add_submodule("ModD", ModD)

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

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 5.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 6.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 7.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 10.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 11.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 12.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 15.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 16.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 17.0)

    def test_nested(self):
        s = brica1.VirtualTimeScheduler()
        ca = brica1.CognitiveArchitecture(s)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 2.0
        CompB.offset = 0.0
        CompC.offset = 1.0

        CompA.interval = 5.0
        CompB.interval = 5.0
        CompC.interval = 5.0

        ModA = brica1.Module()
        ModB = brica1.Module()
        ModC = brica1.Module()

        SupA = brica1.Module()
        SupB = brica1.Module()
        SupC = brica1.Module()

        Top = brica1.Module()

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)

        ModA.make_out_port("out", 3)
        ModB.make_in_port("in", 3)
        ModB.make_out_port("out", 3)
        ModC.make_in_port("in", 3)

        SupA.make_out_port("out", 3)
        SupB.make_in_port("in", 3)
        SupB.make_out_port("out", 3)
        SupC.make_in_port("in", 3)

        SupA.add_submodule("ModA", ModA)
        SupB.add_submodule("ModB", ModB)
        SupC.add_submodule("ModC", ModC)

        ModA.add_component("CompA", CompA)
        ModB.add_component("CompB", CompB)
        ModC.add_component("CompC", CompC)

        # Out ports must be aliased inside-out
        CompA.alias_out_port(ModA, "out", "out")
        ModA.alias_out_port(SupA, "out", "out")

        # In ports must be aliased outside-in
        ModB.alias_in_port(SupB, "in", "in")
        CompB.alias_in_port(ModB, "in", "in")

        # Out ports must be aliased inside-out
        CompB.alias_out_port(ModB, "out", "out")
        ModB.alias_out_port(SupB, "out", "out")

        # In ports must be aliased outside-in
        ModC.alias_in_port(SupC, "in", "in")
        CompC.alias_in_port(ModC, "in", "in")

        SupB.connect(SupA, "out", "in")
        SupC.connect(SupB, "out", "in")

        Top.add_submodule("SupA", SupA)
        Top.add_submodule("SupB", SupB)
        Top.add_submodule("SupC", SupC)

        ca.add_submodule("Top", Top)

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
        self.assertTrue((SupA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 5.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 6.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 7.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 10.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 11.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 12.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 15.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 16.0)

        time = ca.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupA.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupB.get_in_port("in").buffer    == v).all())
        self.assertTrue((SupB.get_out_port("out").buffer  == v).all())
        self.assertTrue((SupC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 17.0)

if __name__ == '__main__':
    test_classes = [VirtualTimeSyncSchedulerTest, VirtualTimeSchedulerTest]

    suites_list = []

    loader = unittest.TestLoader()

    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    all_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(all_suite)
