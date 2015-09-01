##!/bin/sh
git clone https://github.com/karpathy/NeuralTalk.git
mv NeuralTalk/imagernn .
wget http://cs.stanford.edu/people/karpathy/neuraltalk/flickr8k_cnn_lstm_v1.zip
unzip flickr8k_cnn_lstm_v1.zip
python trained_neuraltalk.py NeuralTalk/example_images/vgg_feats.mat NeuralTalk/example_images/tasks.txt flickr8k_cnn_lstm_v1.p
