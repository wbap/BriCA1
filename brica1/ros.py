# -*- coding: utf-8 -*-

"""
ros.py
=====

This module containes classes for ROS integration.

"""

__all__ = ["ROSAdapter"]

# BriCA imports
from .unit import Unit

# ROS imporets
import rospy
from std_msgs.msg import Int16MultiArray, MultiArrayDimension


class ROSAdapter(Unit):
    """
    `ROSAdapter` is a BriCA `Unit` which is intented to provide a bridge over
    the ROS Publisher/Subscriber and BriCA `Agent`.
    """

    def __init__(self, name="BriCA1 Node"):
        """ Create a new `ROSAdapter` instance.

        Args:
          None.

        Returns:
          ROSAdapter: a new `ROSAdapter` instance.

        """

        super(ROSAdapter, self).__init__()
        self.inputs = {}
        self.states = {}
        self.results = {}

        rospy.init_node(name, anonymous=True)

    def setup_subscriber(self, topic, msg_type, id, length, converter):
        """ Setup a ROS subscriber

        Args:
          topic (str): a topic to subscribe to.
          msg_type (msg): incoming message type.
          id (str): a string ID.
          length (int): an initial length of the value vector.

        Returns:
          None.

        """

        self.make_out_port(id, length)

        def callback(data):
            self.get_out_port(id).buffer = converter(data)

        rospy.Subscriber(topic, msg_type, callback)

    def setup_publisher(self, topic, id, length):
        """ Setup a ROS subscriber

        Args:
          topic (str): a topic to subscribe to.
          id (str): a string ID.
          length (int): an initial length of the value vector.

        Returns:
          None.

        """

        self.make_in_port(id, length)
        pub = rospy.Publisher(topic, Int16MultiArray, queue_size=10)

        def callback(data):
            msg = Int16MultiArray()
            msg.data = data
            msg.layout.dim = [MultiArrayDimension("data", 1, length)]
            pub.publish(msg)

        self.get_in_port(id).register_callback(callback)

    def connect(self, target, from_id, to_id):
        """ Connect an out-port of another `Unit` to an in-port.

        Args:
          target (Unit): a `Unit` to connect to.
          from_id (str): an out-port of the target `Unit`.
          to_id(str): an in-port of this `Unit`.

        Returns:
          None.

        """

        super(ROSAdapter, self).connect(target, from_id, to_id)
        from_port = target.get_out_port(from_id)
        to_port = self.get_in_port(to_id)

        def callback(data):
            to_port.sync()
            to_port.invoke_callbacks()

        from_port.register_callback(callback)
