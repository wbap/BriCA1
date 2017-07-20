import sys, os

sys.path.append(os.getcwd())

import numpy as np
import brica1

def test_autostep():
    agent = brica1.Agent()
    scheduler = brica1.VirtualTimeScheduler(agent)

    zero = np.zeros(3, dtype=np.short)
    data = np.array([1, 2, 3], dtype=np.short)

    CompA = brica1.ConstantComponent()
    CompB = brica1.PipeComponent()
    CompC = brica1.NullComponent()

    ModA = brica1.Module()

    ModA.add_component('CompA', CompA)
    ModA.add_component('CompB', CompB)
    ModA.add_component('CompC', CompC)

    CompA.set_state('out', data)
    CompA.make_out_port('out', 3)
    CompB.make_in_port('in', 3)
    brica1.connect((CompA, 'out'), (CompB, 'in'))
    CompB.make_out_port('out', 3)
    CompB.set_map('in', 'out')
    CompC.make_in_port('in', 3)
    brica1.connect((CompB, 'out'), (CompC, 'in'))

    agent.add_submodule('ModA', ModA)

    scheduler.update()

    a_out = zero
    b_in = zero
    b_out = zero
    c_in = zero

    assert (CompA.get_state('out') == data).all()
    assert CompA.get_state('out') is not data

    while True:
        assert (CompA.get_out_port('out').buffer == a_out).all()
        assert (CompB.get_in_port('in').buffer   == b_in ).all()
        assert (CompB.get_out_port('out').buffer == b_out).all()
        assert (CompC.get_in_port('in').buffer   == c_in ).all()

        time = scheduler.step()

        if time > 2000:
            break

        if time == 1000:
            a_out = data
        if time == 1000:
            b_in = data
        if time == 2000:
            b_out = data
        if time == 2000:
            c_in = data

def test_interval():
    agent = brica1.Agent()
    scheduler = brica1.VirtualTimeScheduler(agent)

    zero = np.zeros(3, dtype=np.short)
    data = np.array([1, 2, 3], dtype=np.short)

    CompA = brica1.ConstantComponent()
    CompB = brica1.PipeComponent()
    CompC = brica1.NullComponent()

    ModA = brica1.Module()

    ModA.add_component('CompA', CompA)
    ModA.add_component('CompB', CompB)
    ModA.add_component('CompC', CompC)

    CompA.set_state('out', data)
    CompA.make_out_port('out', 3)
    CompB.make_in_port('in', 3)
    brica1.connect((CompA, 'out'), (CompB, 'in'))
    CompB.make_out_port('out', 3)
    CompB.set_map('in', 'out')
    CompC.make_in_port('in', 3)
    brica1.connect((CompB, 'out'), (CompC, 'in'))

    agent.add_submodule('ModA', ModA)

    scheduler.update()

    a_out = zero
    b_in = zero
    b_out = zero
    c_in = zero

    assert (CompA.get_state('out') == data).all()
    assert CompA.get_state('out') is not data

    interval = 100
    steps = 0

    while True:
        assert (CompA.get_out_port('out').buffer == a_out).all()
        assert (CompB.get_in_port('in').buffer   == b_in ).all()
        assert (CompB.get_out_port('out').buffer == b_out).all()
        assert (CompC.get_in_port('in').buffer   == c_in ).all()
        assert steps * interval == scheduler.current_time

        time = scheduler.step(interval)
        steps += 1

        if time > 2000:
            break

        if time == 1000:
            a_out = data
        if time == 1000:
            b_in = data
        if time == 2000:
            b_out = data
        if time == 2000:
            c_in = data
