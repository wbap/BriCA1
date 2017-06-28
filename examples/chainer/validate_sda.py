#!/usr/bin/env python
import argparse
import numpy as np
from chainer import Variable, FunctionSet, optimizers, cuda
import chainer.functions as F
import data
import cPickle as pickle

import brica1
from chainer_sda import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chainer-BriCA integration")
    parser.add_argument("--gpu", "-g", default=-1, type=int, help="GPU ID")

    args = parser.parse_args()

    use_gpu = False
    if args.gpu >= 0:
        print "Using gpu: {}".format(args.gpu)
        use_gpu = True
        cuda.get_device(args.gpu).use()

    batchsize = 100

    mnist = data.load_mnist_data()
    mnist['data'] = mnist['data'].astype(np.float32)
    mnist['data'] /= 255
    mnist['target'] = mnist['target'].astype(np.int32)

    N_train = 60000
    x_train, x_test = np.split(mnist['data'],   [N_train])
    y_train, y_test = np.split(mnist['target'], [N_train])
    N_test = y_test.size

    f = open('sda.pkl', 'rb')
    stacked_autoencoder = pickle.load(f)
    f.close()

    scheduler = brica1.VirtualTimeSyncScheduler()
    agent = brica1.Agent(scheduler)
    module = brica1.Module()
    module.add_component("stacked_autoencoder", stacked_autoencoder)
    agent.add_submodule("module", module)

    time = 0.0

    sum_loss1 = 0
    sum_loss2 = 0
    sum_loss3 = 0
    sum_loss4 = 0
    sum_accuracy = 0

    for batchnum in xrange(0, N_test, batchsize):
        x_batch = x_test[batchnum:batchnum+batchsize]
        y_batch = y_test[batchnum:batchnum+batchsize]

        stacked_autoencoder.get_in_port("input").buffer = x_batch
        stacked_autoencoder.get_in_port("target").buffer = y_batch

        time = agent.step()

        loss1 = stacked_autoencoder.get_out_port("loss1").buffer
        loss2 = stacked_autoencoder.get_out_port("loss2").buffer
        loss3 = stacked_autoencoder.get_out_port("loss3").buffer
        loss4 = stacked_autoencoder.get_out_port("loss4").buffer
        accuracy = stacked_autoencoder.get_out_port("accuracy").buffer

        sum_loss1 += loss1 * batchsize
        sum_loss2 += loss2 * batchsize
        sum_loss3 += loss3 * batchsize
        sum_loss4 += loss4 * batchsize
        sum_accuracy += accuracy * batchsize

    mean_loss1 = sum_loss1 / N_test
    mean_loss2 = sum_loss2 / N_test
    mean_loss3 = sum_loss3 / N_test
    mean_loss4 = sum_loss3 / N_test
    mean_accuracy = sum_accuracy / N_test

    print "Validation\tLoss1: {}\tLoss2: {}\tLoss3: {}\tLoss4: {}\tAccuracy: {}".format(mean_loss1, mean_loss2, mean_loss3, mean_loss4, mean_accuracy)
