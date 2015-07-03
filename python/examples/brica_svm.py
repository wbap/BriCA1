#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

import brica1

# SVM Component Definition
class SVMComponent(brica1.Component):
    def __init__(self, n_in):
        super(SVMComponent, self).__init__()
        self.classifier = svm.LinearSVC(C=1.0)
        self.make_in_port("in0", n_in)
        self.make_out_port("out0", 1)

    def fire(self):
        x = self.inputs["in0"]
        z = self.classifier.predict([x])
        self.results["out0"] = z

    def fit(self, X, y):
        self.classifier.fit(X, y)

# Load iris dataset
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target

# Setup data feeder component
feeder = brica1.ConstantComponent()
feeder.make_out_port("out0", 2)

# Setup SVM component
svm = SVMComponent(2)
svm.fit(X, y)

# Connect the components
brica1.connect((feeder, "out0"), (svm, "in0"))

# Add components to module
mod = brica1.Module()
mod.add_component("feeder", feeder)
mod.add_component("svm", svm)

# Setup scheduler and agent
s = brica1.VirtualTimeSyncScheduler()
a = brica1.Agent(s)
a.add_submodule("mod", mod)

# Test the classifier
for i in xrange(len(X)):
    feeder.set_state("out0", X[i]) # Set data feeder to training data i

    a.step() # Execute prediction

    print "Actual: {}\tPrediction: {}\t{}".format(y[i], svm.get_out_port("out0").buffer[0], y[i] == svm.get_out_port("out0").buffer[0])
