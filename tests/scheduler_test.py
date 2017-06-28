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

    def test_set(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=100)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompSet = brica1.ComponentSet()
        CompSet.add_component("CompA", CompA, 0)
        CompSet.add_component("CompB", CompB, 1)
        CompSet.add_component("CompC", CompC, 2)

        ModA = brica1.Module()
        ModA.add_component("CompSet", CompSet)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())

    def test_component(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=100)

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
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())

    def test_module(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=100)

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

        brica1.alias_out_port((ModA, "out"), (CompA, "out"))
        brica1.alias_in_port((ModB, "in"), (CompB, "in"))
        brica1.alias_out_port((ModB, "out"), (CompB, "out"))
        brica1.alias_in_port((ModC, "in"), (CompC, "in"))

        brica1.connect((ModA, "out"), (ModB, "in"))
        brica1.connect((ModB, "out"), (ModC, "in"))

        ModD.add_submodule("ModA", ModA)
        ModD.add_submodule("ModB", ModB)
        ModD.add_submodule("ModC", ModC)

        agent.add_submodule("ModD", ModD)

        s.update()

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

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())

    def test_nested(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=100)

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

        # Port aliasing must start from outside-in
        brica1.alias_out_port((SupA, "out"), (ModA, "out"))
        brica1.alias_out_port((ModA, "out"), (CompA, "out"))

        brica1.alias_in_port((SupB, "in"), (ModB, "in"))
        brica1.alias_in_port((ModB, "in"), (CompB, "in"))

        brica1.alias_out_port((SupB, "out"), (ModB, "out"))
        brica1.alias_out_port((ModB, "out"), (CompB, "out"))

        brica1.alias_in_port((SupC, "in"), (ModC, "in"))
        brica1.alias_in_port((ModC, "in"), (CompC, "in"))

        brica1.connect((SupA, "out"), (SupB, "in"))
        brica1.connect((SupB, "out"), (SupC, "in"))

        Top.add_submodule("SupA", SupA)
        Top.add_submodule("SupB", SupB)
        Top.add_submodule("SupC", SupC)

        agent.add_submodule("Top", Top)

        s.update()

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

        s.step()

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

        s.step()

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

        s.step()

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

    def test_callback(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=100)

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
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        def assign_callback(port):
            def callback(v):
                self.assertTrue((port.buffer == v).all())
            port.register_callback(callback)

        assign_callback(CompA.get_out_port("out"))
        assign_callback(CompB.get_in_port("in"))
        assign_callback(CompB.get_out_port("out"))
        assign_callback(CompC.get_in_port("in"))

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())

class VirtualTimeSchedulerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_set(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompSet = brica1.ComponentSet()
        CompSet.add_component("CompA", CompA, 0)
        CompSet.add_component("CompB", CompB, 1)
        CompSet.add_component("CompC", CompC, 2)

        ModA = brica1.Module()
        ModA.add_component("CompSet", CompSet)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())

    def test_component(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 200
        CompB.offset = 000
        CompC.offset = 100

        CompA.interval = 500
        CompB.interval = 500
        CompC.interval = 500

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 700)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1000)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1100)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1200)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v   ).all())
        self.assertEquals(time, 1600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertEquals(time, 1700)

    def test_module(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 200
        CompB.offset = 000
        CompC.offset = 100

        CompA.interval = 500
        CompB.interval = 500
        CompC.interval = 500

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

        brica1.alias_out_port((ModA, "out"), (CompA, "out"))
        brica1.alias_in_port((ModB, "in"), (CompB, "in"))
        brica1.alias_out_port((ModB, "out"), (CompB, "out"))
        brica1.alias_in_port((ModC, "in"), (CompC, "in"))

        brica1.connect((ModA, "out"), (ModB, "in"))
        brica1.connect((ModB, "out"), (ModC, "in"))

        ModD.add_submodule("ModA", ModA)
        ModD.add_submodule("ModB", ModB)
        ModD.add_submodule("ModC", ModC)

        agent.add_submodule("ModD", ModD)

        s.update()

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

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == zero).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 700)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 1000)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 1100)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == zero).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 1200)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v   ).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v   ).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == zero).all())
        self.assertEquals(time, 1500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 1600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertTrue((ModA.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModB.get_in_port("in").buffer    == v).all())
        self.assertTrue((ModB.get_out_port("out").buffer  == v).all())
        self.assertTrue((ModC.get_in_port("in").buffer    == v).all())
        self.assertEquals(time, 1700)

    def test_nested(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 200
        CompB.offset = 000
        CompC.offset = 100

        CompA.interval = 500
        CompB.interval = 500
        CompC.interval = 500

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

        # Port aliasing must start from outside-in
        brica1.alias_out_port((SupA, "out"), (ModA, "out"))
        brica1.alias_out_port((ModA, "out"), (CompA, "out"))

        brica1.alias_in_port((SupB, "in"), (ModB, "in"))
        brica1.alias_in_port((ModB, "in"), (CompB, "in"))

        brica1.alias_out_port((SupB, "out"), (ModB, "out"))
        brica1.alias_out_port((ModB, "out"), (CompB, "out"))

        brica1.alias_in_port((SupC, "in"), (ModC, "in"))
        brica1.alias_in_port((ModC, "in"), (CompC, "in"))

        brica1.connect((SupA, "out"), (SupB, "in"))
        brica1.connect((SupB, "out"), (SupC, "in"))

        Top.add_submodule("SupA", SupA)
        Top.add_submodule("SupB", SupB)
        Top.add_submodule("SupC", SupC)

        agent.add_submodule("Top", Top)

        s.update()

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

        time = s.step()

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
        self.assertEquals(time, 500)

        time = s.step()

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
        self.assertEquals(time, 600)

        time = s.step()

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
        self.assertEquals(time, 700)

        time = s.step()

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
        self.assertEquals(time, 1000)

        time = s.step()

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
        self.assertEquals(time, 1100)

        time = s.step()

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
        self.assertEquals(time, 1200)

        time = s.step()

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
        self.assertEquals(time, 1500)

        time = s.step()

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
        self.assertEquals(time, 1600)

        time = s.step()

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
        self.assertEquals(time, 1700)

    def test_callback(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 200
        CompB.offset = 000
        CompC.offset = 100

        CompA.interval = 500
        CompB.interval = 500
        CompC.interval = 500

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        def assign_callback(port):
            def callback(v):
                self.assertTrue((port.buffer == v).all())
            port.register_callback(callback)

        assign_callback(CompA.get_out_port("out"))
        assign_callback(CompB.get_in_port("in"))
        assign_callback(CompB.get_out_port("out"))
        assign_callback(CompC.get_in_port("in"))

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 700)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1000)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1100)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1200)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())
        self.assertEquals(time, 1500)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v   ).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v   ).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v   ).all())
        self.assertEquals(time, 1600)

        time = s.step()

        self.assertTrue((CompA.get_out_port("out").buffer == v).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == v).all())
        self.assertTrue((CompB.get_out_port("out").buffer == v).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == v).all())
        self.assertEquals(time, 1700)

    def test_interval(self):
        agent = brica1.Agent()
        s = brica1.VirtualTimeScheduler(agent)

        zero = numpy.zeros(3, dtype=numpy.short)
        v = numpy.array([1, 2, 3], dtype=numpy.short)

        CompA = brica1.ConstantComponent()
        CompB = brica1.PipeComponent()
        CompC = brica1.NullComponent()

        CompA.offset = 200
        CompB.offset = 000
        CompC.offset = 100

        CompA.interval = 500
        CompB.interval = 500
        CompC.interval = 500

        ModA = brica1.Module()

        ModA.add_component("CompA", CompA)
        ModA.add_component("CompB", CompB)
        ModA.add_component("CompC", CompC)

        CompA.set_state("out", v)
        CompA.make_out_port("out", 3)
        CompB.make_in_port("in", 3)
        brica1.connect((CompA, "out"), (CompB, "in"))
        CompB.make_out_port("out", 3)
        CompB.set_map("in", "out")
        CompC.make_in_port("in", 3)
        brica1.connect((CompB, "out"), (CompC, "in"))

        agent.add_submodule("ModA", ModA)

        s.update()

        n_steps = 0

        self.assertTrue((CompA.get_state("out") == v).all())
        self.assertIsNot(CompA.get_state("out"), v)

        self.assertTrue((CompA.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompB.get_in_port("in").buffer   == zero).all())
        self.assertTrue((CompB.get_out_port("out").buffer == zero).all())
        self.assertTrue((CompC.get_in_port("in").buffer   == zero).all())

        a_out = zero
        b_in = zero
        b_out = zero
        c_in = zero

        time = 0
        interval = 1

        while time < 1700:
            time = s.step(interval)
            n_steps += 1

            if time == 700:
                a_out = v

            if time == 1000:
                b_in = v

            if time == 1500:
                b_out = v

            if time == 1600:
                c_in = v

            self.assertTrue((CompA.get_out_port("out").buffer == a_out).all())
            self.assertTrue((CompB.get_in_port("in").buffer   == b_in ).all())
            self.assertTrue((CompB.get_out_port("out").buffer == b_out).all())
            self.assertTrue((CompC.get_in_port("in").buffer   == c_in  ).all())
            self.assertEquals(time, n_steps * interval)

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
