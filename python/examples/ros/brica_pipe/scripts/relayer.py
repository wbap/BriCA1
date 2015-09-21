#!/usr/bin/env python
import numpy as np
import brica1
import brica1.ros
import rospy
from std_msgs.msg import Int16MultiArray, MultiArrayDimension

def relayer():
    Comp = brica1.PipeComponent()
    Comp.make_in_port("in", 3)
    Comp.make_out_port("out", 3)
    Comp.set_map("in", "out")

    Mod = brica1.Module()
    Mod.make_in_port("in", 3)
    Mod.make_out_port("out", 3)
    Mod.add_component("Comp", Comp)

    Scheduler = brica1.RealTimeSyncScheduler()
    Agent = brica1.Agent(Scheduler)
    Agent.make_in_port("in", 3)
    Agent.make_out_port("out", 3)
    Agent.add_submodule("Mod", Mod)

    brica1.alias_in_port((Agent, "in"), (Mod, "in"))
    brica1.alias_out_port((Agent, "out"), (Mod, "out"))
    brica1.alias_in_port((Mod, "in"), (Comp, "in"))
    brica1.alias_out_port((Mod, "out"), (Comp, "out"))

    def converter(msg):
        return np.array(list(msg.data), dtype=np.int16)

    Adapter = brica1.ros.ROSAdapter("relayer")
    Adapter.setup_subscriber("chatter0", Int16MultiArray, "out", 3, converter)
    Adapter.setup_publisher("chatter1", "in", 3)

    brica1.connect((Adapter, "out"), (Agent, "in"))
    brica1.connect((Agent, "out"), (Adapter, "in"))

    while not rospy.is_shutdown():
        Agent.step()
        print "Agent in port:  {}".format(Agent.get_in_port("in").buffer)
        print "Agent out port: {}".format(Agent.get_out_port("out").buffer)

if __name__ == '__main__':
    try:
        relayer()
    except rospy.ROSInterruptException:
        pass
