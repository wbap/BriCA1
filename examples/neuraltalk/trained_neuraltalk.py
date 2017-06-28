#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cPickle as pickle
import numpy
import scipy.io
import brica1

from imagernn.imagernn_utils import decodeGenerator, eval_split

class IntComponent(brica1.Component):
    def __init__(self, maximum=16):
        super(IntComponent, self).__init__()
        self.index = 0
        self.maximum = maximum

    def fire(self):
        for id in self.out_ports.keys():
            self.results[id] = numpy.array([self.index], dtype=numpy.int16)

        self.index = (self.index + 1) % self.maximum

class CNNComponent(brica1.Component):
    def __init__(self, matfile):
        super(CNNComponent, self).__init__()
        features_struct = scipy.io.loadmat(matfile)
        self.features = features_struct["feats"]

    def fire(self):
        self.results["out"] = self.features[:, self.inputs["in"][0]]

class RNNComponent(brica1.Component):
    def __init__(self, cpfile, taskfile):
        super(RNNComponent, self).__init__()
        checkpoint = pickle.load(open(cpfile, "rb"))
        self.params = checkpoint["params"]
        self.dataset = self.params["dataset"]
        self.model = checkpoint["model"]
        self.misc = {}
        self.misc["wordtoix"] = checkpoint["wordtoix"]
        self.ixtoword = checkpoint["ixtoword"]
        self.BatchGenerator = decodeGenerator(self.params)
        self.img_names = open(taskfile, "r").read().splitlines()

    def fire(self):
        img = {}
        img["feat"] = self.inputs["in"]
        img["local_file_path"] = "hoge"

        if img["feat"].shape[0] != 4096:
            return

        kwparams = {'beam_size': 1}
        Ys = self.BatchGenerator.predict([{"image": img}], self.model, self.params, **kwparams)

        top_predictions = Ys[0]
        top_prediction = top_predictions[0]
        candidate = " ".join([self.ixtoword[ix] for ix in top_prediction[1] if ix > 0])
        print candidate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('matfile', type=str, help='the vgg_feats.mat file')
    parser.add_argument('taskfile', type=str, help='the tasks.txt file')
    parser.add_argument('cpfile', type=str, help='the input checkpoint')
    parser.add_argument('-b', '--beam_size', type=int, default=1, help='beam size in inference. 1 indicates greedy per-word max procedure. Good value is approx 20 or so, and more = better.')

    args = parser.parse_args()
    params = vars(args)

    num = IntComponent()
    cnn = CNNComponent(params["matfile"])
    rnn = RNNComponent(params["cpfile"], params["taskfile"])

    num.offset = 0.0
    cnn.offset = 1.0
    rnn.offset = 2.0

    num.interval = 3.0
    cnn.interval = 3.0
    rnn.interval = 3.0

    mod = brica1.Module()
    mod.add_component("num", num)
    mod.add_component("cnn", cnn)
    mod.add_component("rnn", rnn)

    num.make_out_port("out", 1)
    cnn.make_in_port("in", 1)
    cnn.make_out_port("out", 1)
    rnn.make_in_port("in", 1)

    brica1.connect((num, "out"), (cnn, "in"))
    brica1.connect((cnn, "out"), (rnn, "in"))

    s = brica1.VirtualTimeScheduler()
    ca = brica1.Agent(s)

    ca.add_submodule("mod", mod)

    for _ in xrange(16):
        ca.step()
        ca.step()
        ca.step()
