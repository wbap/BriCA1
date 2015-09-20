#!/bin/sh
if [ ! -e data.py ]; then
    wget https://raw.githubusercontent.com/pfnet/chainer/master/examples/mnist/data.py
fi
python chainer_sda.py --gpu 0
