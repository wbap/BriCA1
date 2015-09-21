#!/usr/bin/env python
import argparse
import numpy as np
from chainer import Variable, FunctionSet, optimizers, cuda
import chainer.functions as F
import data
import cPickle as pickle

import brica1

class SLP(FunctionSet):
    def __init__(self, n_input, n_output):
        super(SLP, self).__init__(
            transform=F.Linear(n_input, n_output)
        )

    def forward(self, x_data, y_data):
        x = Variable(x_data)
        t = Variable(y_data)
        y = F.sigmoid(self.transform(x))
        loss = F.softmax_cross_entropy(y, t)
        accuracy = F.accuracy(y, t)
        return loss, accuracy

    def predict(self, x_data):
        x = Variable(x_data)
        y = F.sigmoid(self.transform(x))
        return y.data

class Autoencoder(FunctionSet):
    def __init__(self, n_input, n_output):
        super(Autoencoder, self).__init__(
            encoder=F.Linear(n_input, n_output),
            decoder=F.Linear(n_output, n_input)
        )

    def forward(self, x_data):
        x = Variable(x_data)
        t = Variable(x_data)
        x = F.dropout(x)
        h = F.sigmoid(self.encoder(x))
        y = F.sigmoid(self.decoder(h))
        loss = F.mean_squared_error(y, t)
        return loss

    def encode(self, x_data):
        x = Variable(x_data)
        h = F.sigmoid(self.encoder(x))
        return h.data

class SLPComponent(brica1.Component):
    def __init__(self, n_input, n_output, use_gpu=False):
        super(SLPComponent, self).__init__()
        self.model = SLP(n_input, n_output)
        self.optimizer = optimizers.Adam()
        self.training = True

        self.make_in_port("input", n_input)
        self.make_in_port("target", 1)
        self.make_out_port("output", n_output)
        self.make_out_port("loss", 1)
        self.make_out_port("accuracy", 1)

        self.use_gpu = use_gpu

        if self.use_gpu:
            self.model.to_gpu()

        self.optimizer.setup(self.model)

    def to_cpu(self):
        if self.use_gpu:
            self.model.to_cpu()
            self.optimizer.setup(self.model)
            self.use_gpu = False

    def to_gpu(self):
        if not self.use_gpu:
            self.model.to_gpu()
            self.optimizer.setup(self.model)
            self.use_gpu = True

    def set_training(self, flag):
        self.training = flag;

    def fire(self):
        x_data = self.inputs["input"].astype(np.float32)
        t_data = self.inputs["target"].astype(np.int32)

        if self.use_gpu:
            x_data = cuda.to_gpu(x_data)
            t_data = cuda.to_gpu(t_data)

        self.optimizer.zero_grads()
        loss, accuracy = self.model.forward(x_data, t_data)
        if self.training:
            loss.backward()
            self.optimizer.update()

        y_data = self.model.predict(x_data)

        self.results["loss"] = cuda.to_cpu(loss.data)
        self.results["accuracy"] = cuda.to_cpu(accuracy.data)
        self.results["output"] = cuda.to_cpu(y_data)

class AutoencoderComponent(brica1.Component):
    def __init__(self, n_input, n_output, use_gpu=False):
        super(AutoencoderComponent, self).__init__()
        self.model = Autoencoder(n_input, n_output)
        self.optimizer = optimizers.Adam()
        self.training = True

        self.make_in_port("input", n_input)
        self.make_out_port("output", n_output)
        self.make_out_port("loss", 1)

        self.use_gpu = use_gpu

        if self.use_gpu:
            self.model.to_gpu()

        self.optimizer.setup(self.model)

    def to_cpu(self):
        if self.use_gpu:
            self.model.to_cpu()
            self.optimizer.setup(self.model)
            self.use_gpu = False

    def to_gpu(self):
        if not self.use_gpu:
            self.model.to_gpu()
            self.optimizer.setup(self.model)
            self.use_gpu = True

    def set_training(self, flag):
        self.training = flag;

    def fire(self):
        x_data = self.inputs["input"].astype(np.float32)

        if self.use_gpu:
            x_data = cuda.to_gpu(x_data)


        self.optimizer.zero_grads()
        loss = self.model.forward(x_data)
        if self.training:
            loss.backward()
            self.optimizer.update()

        y_data = self.model.encode(x_data)

        self.results["loss"] = cuda.to_cpu(loss.data)
        self.results["output"] = cuda.to_cpu(y_data)

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
    n_epoch = 20

    mnist = data.load_mnist_data()
    mnist['data'] = mnist['data'].astype(np.float32)
    mnist['data'] /= 255
    mnist['target'] = mnist['target'].astype(np.int32)

    N_train = 60000
    x_train, x_test = np.split(mnist['data'],   [N_train])
    y_train, y_test = np.split(mnist['target'], [N_train])
    N_test = y_test.size

    autoencoder1 = AutoencoderComponent(28**2, 1000, use_gpu=use_gpu)
    autoencoder2 = AutoencoderComponent(1000, 1000, use_gpu=use_gpu)
    autoencoder3 = AutoencoderComponent(1000, 1000, use_gpu=use_gpu)
    slp = SLPComponent(1000, 10)

    brica1.connect((autoencoder1, "output"), (autoencoder2, "input"))
    brica1.connect((autoencoder2, "output"), (autoencoder3, "input"))
    brica1.connect((autoencoder3, "output"), (slp, "input"))

    stacked_autoencoder = brica1.ComponentSet()
    stacked_autoencoder.add_component("autoencoder1", autoencoder1, 1)
    stacked_autoencoder.add_component("autoencoder2", autoencoder2, 2)
    stacked_autoencoder.add_component("autoencoder3", autoencoder3, 3)
    stacked_autoencoder.add_component("slp", slp, 4)

    stacked_autoencoder.make_in_port("input", 28**2)
    stacked_autoencoder.make_in_port("target", 1)
    stacked_autoencoder.make_out_port("output", 1000)
    stacked_autoencoder.make_out_port("loss1", 1)
    stacked_autoencoder.make_out_port("loss2", 1)
    stacked_autoencoder.make_out_port("loss3", 1)
    stacked_autoencoder.make_out_port("loss4", 1)
    stacked_autoencoder.make_out_port("accuracy", 1)

    brica1.alias_in_port((stacked_autoencoder, "input"), (autoencoder1, "input"))
    brica1.alias_out_port((stacked_autoencoder, "output"), (slp, "output"))
    brica1.alias_out_port((stacked_autoencoder, "loss1"), (autoencoder1, "loss"))
    brica1.alias_out_port((stacked_autoencoder, "loss2"), (autoencoder2, "loss"))
    brica1.alias_out_port((stacked_autoencoder, "loss3"), (autoencoder3, "loss"))
    brica1.alias_out_port((stacked_autoencoder, "loss4"), (slp, "loss"))
    brica1.alias_out_port((stacked_autoencoder, "accuracy"), (slp, "accuracy"))
    brica1.alias_in_port((stacked_autoencoder, "target"), (slp, "target"))

    scheduler = brica1.VirtualTimeSyncScheduler()
    agent = brica1.Agent(scheduler)
    module = brica1.Module()
    module.add_component("stacked_autoencoder", stacked_autoencoder)
    agent.add_submodule("module", module)

    time = 0.0

    for epoch in xrange(n_epoch):
        perm = np.random.permutation(N_train)
        sum_loss1 = 0
        sum_loss2 = 0
        sum_loss3 = 0
        sum_loss4 = 0
        sum_accuracy = 0

        for batchnum in xrange(0, N_train, batchsize):
            x_batch = x_train[perm[batchnum:batchnum+batchsize]]
            y_batch = y_train[perm[batchnum:batchnum+batchsize]]

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

        mean_loss1 = sum_loss1 / N_train
        mean_loss2 = sum_loss2 / N_train
        mean_loss3 = sum_loss3 / N_train
        mean_loss4 = sum_loss3 / N_train
        mean_accuracy = sum_accuracy / N_train

        print "Epoch: {}\tLoss1: {}\tLoss2: {}\tLoss3: {}\tLoss4: {}\tAccuracy: {}".format(epoch+1, mean_loss1, mean_loss2, mean_loss3, mean_loss4, mean_accuracy)

    autoencoder1.reset()
    autoencoder2.reset()
    autoencoder3.reset()
    slp.reset()
    stacked_autoencoder.reset()

    autoencoder1.set_training(False)
    autoencoder2.set_training(False)
    autoencoder3.set_training(False)
    slp.set_training(False)

    f = open('sda.pkl', 'wb')
    pickle.dump(stacked_autoencoder, f)
    f.close()
