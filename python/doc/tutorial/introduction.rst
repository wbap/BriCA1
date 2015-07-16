Introduction
============

Welcome to the tutorial for Brain-inspired Computing Architecture (BriCA) Version 1. Basics for installing and getting started with the BriCA platform are included in this tutorial. For more advanced content, take a look at some of the other tutorials.

What is BriCA?
--------------

Some introduction...

Installing
----------

BriCA must currently be installed from source which is hosted on `GitHub <http:s//github.com/wbap/V1/>`_. The NumPy library is required to use the library.

1. ``git clone https://github.com/wbap/V1.git``
2. ``cd V1/python``
3. ``sudo python setup.py install`` or ``python setup.py install --user``

Voila! You are done. Now that the library is installed, try running the test code.

``python tests/scheduler_test.py``

This will run four tests, all of which should successfully pass.


Getting Started
---------------

Before starting to write a full featured cognitive architecture there are a number of core concepts you need to know. Here we cover the very basics: ``Components``, ``Modules``, ``Schedulers``, and ``Agents``. The source code for this and all of the other tutorials are included in the ``V1/python/examples`` directory so make sure to check them out.

Components
~~~~~~~~~~

The most fundamental building blocks for a BriCA agent are the ``Components``. A single component has an input port array, output port array, internal states, and a ``fire()`` method which defines its behaviour. For example, if you want to stack a number of denoising autoencoders to perform a trivial MNIST digit classification, you might want to define a ``AutoencoderComponent`` class which implements an autoencoder internally and trains itself based on the input data. In this case, the ``fire()`` method should have some code for online training and *encoding* the input to the learnt representation. In order to stack these autoencoders, input ports may be connected to output ports which are synchronized on different timings based on which ``Scheduler`` is being used. An actual implementation of the autoencoder will appear in the "Stacked Denoising Autoencoder" tutorial. Before we get hands on with complicated ``Components``, we will start by connecting three simple ``Components``: ``ConstantComponent``, ``PipeComponent``, and ``NullComponent`` which are prepared inside the BriCA library.

The ``Components`` are pretty much self explanatory. ``ConstantComponent`` will constantly emit a value which is set in the internal state buffer. ``PipeComponent`` will redirect whatever is in the input port array to the output port array, based on registered associations (called a ``map``). ``NullComponent`` will simply receive a value and do nothing else at all. By connecting these three ``Components``, we can understand how information travels through the BriCA architecture.

First, start by importing the BriCA and NumPy libraries.

  >>> import numpy as np
  >>> import brica1

This will import all submodules into the ``brica1`` namespace. Next, instantiate the three ``Components``.

  >>> CompA = brica1.ConstantComponent()
  >>> CompB = brica1.PipeComponent()
  >>> CompC = brica1.NullComponent()

Create the in/out ports for passing the information.

  >>> CompA.make_out_port("out", 3)
  >>> CompB.make_in_port("in", 3)
  >>> CompB.make_out_port("out", 3)
  >>> CompC.make_in_port("in", 3)

To connect these ``Components``, either the ``brica1.connect()`` method or ``brica1.Component.connect()`` method can be called. The former is highly suggested as it is syntactically intuitive. The out-port of the first ``Component`` is connected to the in-port of the second ``Component``.

  >>> brica1.connect((CompA, "out"), (CompB, "in"))
  >>> brica1.connect((CompB, "out"), (CompC, "in"))

Now see what values are in the ports of the ``Components``.

  >>> CompA.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompC.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)

As you can see, every port is zero-initialized. Lets setup ``CompA`` so it will emit a non-zero vector. Because the ``fire()`` method from ``CompA`` will copy values from ``CompA.states`` into ``CompA.results``, and the contents of ``CompA.results`` will later be dumped to the out-ports, we set the ``CompA.states["out"]`` to the desired value.

  >>> v = np.array([1, 2, 3], dtype=np.int16)
  >>> CompA.set_state("out", v)

So now when we call ``CompA.fire()``, you can see that ``CompA.states["out"]`` is copied to ``CompA.results["out"]``, but not to the out-port.

  >>> CompA.fire()
  >>> CompA.get_result("out")
  array([1, 2, 3], dtype=int16)
  >>> CompA.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)

Calling the ``CompA.output()`` method will flush the contents of ``CompA.results["out"]`` to the out-port with the ID ``"out"``. The ``output()`` method requires a time passed as an argument.

  >>> CompA.output(0.0)
  >>> CompA.get_result("out")
  array([1, 2, 3], dtype=int16)
  >>> CompA.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)

However, the information is not yet passed to ``CompB``. In order to pass the contents of ``CompA`` out-ports to ``CompB`` in-ports, ``CompB.input()`` must be called. This will also automatically copy the values of in-ports to ``CompB.inputs``.

  >>> CompB.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.inputs["in"]
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  KeyError: 'in'
  >>> CompB.input(0.0)
  >>> CompB.get_in_port("in").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.inputs["in"]
  array([1, 2, 3], dtype=int16)

As ``CompB`` implements a method to bypass the inputs to outputs, calling ``CompB.fire()`` should perform this task... right? Actually, this is not the case.

  >>> CompB.get_result("out")
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/usr/local/lib/python2.7/site-packages/brica1-1.0.0dev_r0-py2.7.egg/brica1/component.py", line 147, in get_result
      return self.results[id]
  KeyError: 'out'
  >>> CompB.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)

This is because ``CompB`` does not yet know which input should be mapped to which output. We set an association with ``CompB.set_map()`` method so it can now map ``CompB.inputs["in"]`` to ``CompB.outputs["out"]``.

  >>> CompB.set_map("in", "out")
  >>> CompB.fire()
  >>> CompB.get_result("out")
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)

And like before, call ``CompB.output()``, then ``CompC.input()`` to pass the information to ``CompC``.

  >>> CompB.output(0.0)
  >>> CompB.get_result("out")
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompC.input(0.0)
  >>> CompC.get_in_port("in").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompC.inputs["in"]
  array([1, 2, 3], dtype=int16)

In practice, ``input()``, ``fire()``, and ``output()`` methods are called by the ``Scheduler`` and handled automatically. Wwhen designing a ``Component``, keep in mind what in/out port names to use and how/when these data are visible from the ``fire()`` method. We highly suggest taking a look at ``brica1/component.py`` so you can see what the three ``Components`` used here do internally.


Modules
~~~~~~~

When you want to build a complex network of ``Components``, there may be times where you would like to group together multiple ``Components`` into a single container. A ``Module`` is a class that serves such task. Assuming you are continuing from the tutorial above, let us start by instantiating a ``Module``.

  >>> ModA = brica1.Module()

The basic functionalities of a ``Module`` are identical to ``Components``: they have input/output port arrays and can be connected via the same interface. The biggest difference is that ``Modules`` can contain ``Modules`` and ``Components`` to create hierarchical structures. The following code adds the ``Components`` defined above to ``ModA``.

  >>> ModA.add_component("CompA", CompA)
  >>> ModA.add_component("CompB", CompB)
  >>> ModA.add_component("CompC", CompC)
  >>> ModA.get_all_components()
  [<brica1.component.NullComponent object at 0x10d156d10>, <brica1.component.PipeComponent object at 0x10d156ed0>, <brica1.component.ConstantComponent object at 0x10d156c50>]

The top-level ``Module`` which encapsulates an entire cognitive architecture is called an ``Agent``, which is combined with the ``Scheduler`` to adapt to various tasks. We will go over ``Schedulers`` and ``Agents`` more in detail below.


Schedulers
~~~~~~~~~~

There are four types of ``Schedulers`` planned and two of them currently implemented: the ``VirtualTimeSyncScheduler`` sychronously calls ``input()``, ``fire()``, then ``output()`` methods of all encapsulated ``Components`` in order. ``VirtualTimeScheduler`` calls these methods according to the ``offset`` and ``interval`` property values of each ``Component``.


Agents
~~~~~~

Beacause the implementation is simpler, we will show some examples for using the ``VirtualTimeSyncScheduler`` in this tutorial. Instantiate the ``Scheduler`` and pass it to the ``Agent`` constructor.

  >>> s = brica1.VirtualTimeSyncScheduler()
  >>> agent = brica1.Agent(s)

Adding a ``Module`` to the ``Agent`` will automatically make the ``Scheduler`` aware of all ``Components`` contained in the ``Module``. First re-setup the ``Components`` and ``Modules``.

  >>> CompA = brica1.ConstantComponent()
  >>> CompB = brica1.PipeComponent()
  >>> CompC = brica1.NullComponent()
  >>> CompB.set_map("in", "out")
  >>> CompA.make_out_port("out", 3)
  >>> CompB.make_in_port("in", 3)
  >>> CompB.make_out_port("out", 3)
  >>> CompC.make_in_port("in", 3)
  >>> brica1.connect((CompA, "out"), (CompB, "in"))
  >>> brica1.connect((CompB, "out"), (CompC, "in"))
  >>> v = np.array([1, 2, 3], dtype=np.int16)
  >>> CompA.set_state("out", v)
  >>> ModA = brica1.Module()
  >>> ModA.add_component("CompA", CompA)
  >>> ModA.add_component("CompB", CompB)
  >>> ModA.add_component("CompC", CompC)
  >>> agent.add_submodule("ModA", ModA)

First check that all ports for every ``Component`` is initialized with a zero vector.

  >>> CompA.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompC.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)

Call the ``step()`` method of ``Agent`` to update the ``Components``. Because the ``Scheduler`` given to the ``Agent`` is ``VirtualTimeSyncScheduler``, the ``input()`` method for all ``Components`` are called first, then ``fire()``, and finally the ``output()``.

  >>> agent.step()
  1.0
  >>> CompA.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([0, 0, 0], dtype=int16)
  >>> CompC.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)

  >>> agent.step()
  2.0
  >>> CompA.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_in_port("in").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompC.get_in_port("in").buffer
  array([0, 0, 0], dtype=int16)

  >>> agent.step()
  3.0
  >>> CompA.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_in_port("in").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompB.get_out_port("out").buffer
  array([1, 2, 3], dtype=int16)
  >>> CompC.get_in_port("in").buffer
  array([1, 2, 3], dtype=int16)

The very basics of BriCA V1 have been covered here, proceed to the '``Component`` Definition' tutorial to learn how to create your own ``Components``. This specific tutorial will implement a support vector machine (SVM) and random forest (RF) classifiers and compare its output.
