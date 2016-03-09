from benchmarker import Benchmarker

import brica1

with Benchmarker(width=20, loop=10000, cycle=20) as bench:
    @bench(None)
    def _(bm):
        for _ in bm:
            pass

    @bench('constant_null_small')
    def _(bm):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=1.0)

        compA = brica1.ConstantComponent()
        compB = brica1.NullComponent()
        mod = brica1.Module();

        mod.add_component('compA', compA)
        mod.add_component('compB', compB)

        compA.make_out_port('out', 1)
        compB.make_in_port('in', 1)

        brica1.connect((compA, 'out'), (compB, 'in'))

        agent.add_submodule('mod', mod)

        s.update()

        for _ in bm:
            s.step()

    @bench('constant_null_medium')
    def _(bm):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=1.0)

        compA = brica1.ConstantComponent()
        compB = brica1.NullComponent()
        mod = brica1.Module();

        mod.add_component('compA', compA)
        mod.add_component('compB', compB)

        compA.make_out_port('out', 28)
        compB.make_in_port('in', 28)

        brica1.connect((compA, 'out'), (compB, 'in'))

        agent.add_submodule('mod', mod)

        s.update()

        for _ in bm:
            s.step()

    @bench('constant_null_large')
    def _(bm):
        agent = brica1.Agent()
        s = brica1.VirtualTimeSyncScheduler(agent, interval=1.0)

        compA = brica1.ConstantComponent()
        compB = brica1.NullComponent()
        mod = brica1.Module();

        mod.add_component('compA', compA)
        mod.add_component('compB', compB)

        compA.make_out_port('out', 256*256*3)
        compB.make_in_port('in', 256*256*3)

        brica1.connect((compA, 'out'), (compB, 'in'))

        agent.add_submodule('mod', mod)

        s.update()

        for _ in bm:
            s.step()
