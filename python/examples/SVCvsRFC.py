# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble, svm,datasets
 
import brica1



# Randomforest Component Definition
class RandomForestClassifierComponent(brica1.Component):
    def __init__(self, n_in):
        super(RandomForestClassifierComponent, self).__init__()
        self.classifier = ensemble.RandomForestClassifier()
        self.make_in_port("in0", n_in)
        self.make_out_port("out0", 1)
 
    def fire(self):
        x = self.inputs["in0"]
        z = self.classifier.predict([x])
        self.results["out0"] = z
 
    def fit(self, X, y):
        self.classifier.fit(X, y)


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


# SVM vs RFC Component Definition
class SVMvsRFC_Component(brica1.Component):
    def __init__(self, n_in):
        super(SVMvsRFC_Component, self).__init__()
        self.make_in_port("in0",n_in)
        self.make_in_port("in1",n_in)
        self.make_out_port("out0", 1)
        
    def fire(self):
        x = self.inputs["in0"]
        y = self.inputs["in1"]
        self.results["out0"] = (x==y)

 
# Load iris dataset
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
 
# Setup data feeder component
feeder = brica1.ConstantComponent()
feeder.make_out_port("out0", 2)
 
# Setup  components
svm = SVMComponent(2)
svm.fit(X, y)

RFC = RandomForestClassifierComponent(2)
RFC.fit(X,y)

SR =SVMvsRFC_Component(1)

 
# Connect the components
brica1.connect((feeder, "out0"), (svm, "in0"))
brica1.connect((feeder, "out0"), (RFC, "in0"))
brica1.connect((svm, "out0"), (SR, "in0"))
brica1.connect((RFC, "out0"), (SR, "in1"))
 
# Add components to module
mod = brica1.Module()
mod.add_component("feeder", feeder)
mod.add_component("svm", svm)
mod.add_component("RFC",RFC)
mod.add_component("SR", SR)
 
# Setup scheduler and agent
s = brica1.VirtualTimeSyncScheduler()
a = brica1.Agent(s)
a.add_submodule("mod", mod)
 
# Test the classifier
svm_result=[]
RFC_result=[]
svm_vs_RFC=[]

for i in xrange(len(X)):
    feeder.set_state("out0", X[i]) # Set data feeder to training data i
 
    a.step() # Execute prediction
 
    svm_result.append(svm.get_out_port("out0").buffer[0])
    RFC_result.append(RFC.get_out_port("out0").buffer[0])
    
    a.step()
    
    svm_vs_RFC.append(SR.get_out_port("out0").buffer[0])

for i in xrange(len(X)):
 
    print "SVM: {}\tRFC: {}\tRESULT: {}".format(svm_result[i], RFC_result[i], svm_vs_RFC[i])