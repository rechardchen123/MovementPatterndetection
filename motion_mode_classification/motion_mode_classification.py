# !/usr/bin/env python3
# -*- coding: utf-8 -*
import numpy as np 
from sklearn.metrics import confusion_matrix, accuracy_score
import random
import pickle
import tensorflow as tf  
from sklearn.metrics import f1_score
import keras


#training setting 
batch_size = 100
latent_dim = 800 # the parameter ? please check
change = 10
units = 800 # number unit in the MLP hidden layer
num_filter_ae_cls = [32, 32, 64, 64, 128, 128] #conv_layers and No. of its channels for AE +CLS
num_filter_cls = [] # conv layers and No. of its channel for only cls
num_dense = 0 # number of dense layer in classifier excluding the last layer
kernel_size = (1, 3)
activation = tf.nn.relu
padding = 'same'
strides = 1
pool_size = (1, 2)
num_class = 3 # categories of the classification 
reg_l2 = tf.contrib.layers.l1_regularizer(scale=0.1)
initializer = tf.contrib.layers.xavier_initializer(uniform=True, seed=None, dtype=tf.float32)


#import the data 
filename = ''
with open(filename, 'rb') as f:
    kfold_dataset, X_unlabeled = pickle.load(f)


#encoder network
def encoder_network(latent_dim, num_filter_ae_cls, input_combined, input_labeled):
    encoded_combined = input_combined
    encoded_labeled = input_labeled
    layers_shape = []
    for i in range(len(num_filter_ae_cls)):
        scope_name = 'encoder_set_' + str(i+1)
        with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE, initializer=initializer):
            encoded_combined = tf.layers.conv2d(inputs=encoded_combined, activation=tf.nn.relu,filters=num_filter_ae_cls[i],
                                                name='conv_1', kernel_size=kernel_size, strides=strides,padding=padding)
        
        with tf.variable_scope(scope_name, reuse=True, initializer=initializer):
            encoded_labeled = tf.layers.conv2d(inputs=encoded_labeled, activation=tf.nn.relu, filters=num_filter_ae_cls[i],
            name='conv_1', kernel_size=kernel_size, strides=strides, padding=padding)

        if i % 2 !=0:
            encoded_combined = tf.layers.max_pooling2d(encoded_combined, pool_size=pool_size,
                                                        strides=pool_size, name='pool')
            encoded_labeled = tf.layers.max_pooling2d(encoded_labeled, pool_size=pool_size,
                                                        strides=pool_size, name='pool')
        layers_shape.append(encoded_combined.get_shape().as_list())
    
    layers_shape.append(encoded_combined.get_shape.as_list())
    latent_combined = encoded_combined
    latent_labeled = encoded_labeled

    return latent_combined, latent_labeled, layers_shape

# decoder network
def decoder_network(latent_combined, input_size, kernel_size, padding, activation):
    decoded_combined = latent_combined
    num_filter_ = num_filter_ae_cls[::-1]
    if len(num_filter_) % 2 == 0:
        num_filter_ = sorted(set(num_filter_),reverse=True)
        for i in range(len(num_filter_)):
            decoded_combined = tf.keras.layers.UpSampling2D(name='UpSample', size=pool_size)(decoded_combined)
            scope_name = 'decoder_set_' + str(2*i)
            with tf.variable_scope(scope_name, initializer=initializer):
                decoded_combined = tf.layers.conv2d_transpose(inputs=decoded_combined, activation=activation,
                                                                filters=num_filter_[i],name='deconv_1',
                                                                kernel_size=kernel_size,
                                                                strides=strides, padding=padding)
            scope_name = 'decoder_set_' + str(2*i +1)
            with tf.variable_scope(scope_name, initializer=initializer):
                filter_size, activation=(input_size[-1], tf.nn.sigmoid) if i == len(num_filter_) - 1 else (int(num_filter_[i] / 2), tf.nn.relu)
                if i ==len(num_filter_):
                    kernel_size = (1, input_size[1] - (decoded_combined.get_shape().as_list()[2] - 1) * strides)
                    padding = 'valid'
                decoded_combined = tf.layers.conv2d_transpose(inputs=decoded_combined, activation=activation,
                                                              filters=filter_size, name='deconv_1',
                                                              kernel_size=kernel_size,
                                                              strides=strides, padding=padding)
    else:
        num_filter_ = sorted(set(num_filter_), reverse=True)
        for i in range(len(num_filter_)):
            scope_name = 'decoder_set_' + str(2 * i)
            with tf.variable_scope(scope_name, initializer=initializer):
                decoded_combined = tf.layers.conv2d_transpose(inputs=decoded_combined, activation=activation,
                                                              filters=num_filter_[i], name='deconv_1',
                                                              kernel_size=kernel_size,
                                                              strides=strides, padding=padding)
            scope_name = 'decoder_set_' + str(2 * i + 1)
            with tf.variable_scope(scope_name, initializer=initializer):
                filter_size, activation = (input_size[-1], tf.nn.sigmoid) if i == len(num_filter_) - 1 else (int(num_filter_[i] / 2), tf.nn.relu)
                if i == len(num_filter_): # change it len(num_filter_)-1 if spatial size is not dividable by 2
                    kernel_size = (1, input_size[1] - (decoded_combined.get_shape().as_list()[2] - 1) * strides)
                    padding = 'valid'
                decoded_combined = tf.layers.conv2d_transpose(inputs=decoded_combined, activation=activation,
                                                              filters=filter_size, name='deconv_1',
                                                              kernel_size=kernel_size,
                                                              strides=strides, padding=padding)
                if i != len(num_filter_) - 1:
                    decoded_combined = tf.keras.layers.UpSampling2D(name='UpSample', size=pool_size)(decoded_combined)
    return decoded_combined

def classifier_mlp(latent_labeled, num_class, num_filter_cls, num_dense):
    conv_layer = latent_labeled
    for i in range(len(num_filter_cls)):
        scope_name = 'cls_conv_set_' + str(i + 1)
        with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE, initializer=initializer):
            conv_layer = tf.layers.conv2d(inputs=conv_layer, activation=tf.nn.relu, filters=num_filter_cls[i],
                                          kernel_size=kernel_size, strides=strides, padding=padding,
                                          kernel_initializer=initializer)
        if len(num_filter_cls) % 2 == 0:
            if i % 2 != 0:
                conv_layer = tf.layers.max_pooling2d(conv_layer, pool_size=pool_size,strides=pool_size, name='pool')
        else:
            if i % 2 == 0:
                conv_layer = tf.layers.max_pooling2d(conv_layer, pool_size=pool_size,strides=pool_size, name='pool')

    dense = tf.layers.flatten(conv_layer)
    units = int(dense.get_shape().as_list()[-1] / 4)
    for i in range(num_dense):
        scope_name = 'cls_dense_set_' + str(i + 1)
        with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE, initializer=initializer):
            dense = tf.layers.dense(dense, units, activation=tf.nn.relu, kernel_initializer=initializer)
        units /= 2
    dense_last = dense
    dense = tf.layers.dropout(dense, 0.5)
    scope_name = 'cls_last_dense_'
    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE, initializer=initializer):
        classifier_output = tf.layers.dense(dense, num_class, name='FC_4', kernel_initializer=initializer)
    return classifier_output, dense_last


def semi_supervised(input_labeled, input_combined, true_label, alpha, beta, num_class, latent_dim, num_filter_ae_cls, num_filter_cls, num_dense, input_size):

    latent_combined, latent_labeled, layers_shape = encoder_network(latent_dim=latent_dim, num_filter_ae_cls=num_filter_ae_cls,
                                                                    input_combined=input_combined, input_labeled=input_labeled)
    decoded_output = decoder_network(latent_combined=latent_combined, input_size=input_size, kernel_size=kernel_size, activation=activation, padding=padding)
    classifier_output, dense = classifier_mlp(latent_labeled, num_class, num_filter_cls=num_filter_cls, num_dense=num_dense)
    #classifier_output = classifier_cnn(latent_labeled, num_filter=num_filter)

    loss_ae = tf.reduce_mean(tf.square(input_combined - decoded_output), name='loss_ae') * 100
    loss_cls = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=true_label, logits=classifier_output),
                              name='loss_cls')
    total_loss = alpha*loss_ae + beta*loss_cls
    #total_loss = beta * loss_ae + alpha * loss_cls
    loss_reg = tf.reduce_sum(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES, 'EasyNet'))
    train_op_ae = tf.train.AdamOptimizer().minimize(loss_ae)
    train_op_cls = tf.train.AdamOptimizer().minimize(loss_cls)
    train_op = tf.train.AdamOptimizer().minimize(total_loss)
    # train_op = train_op = tf.layers.optimize_loss(total_loss, optimizer='Adam')

    correct_prediction = tf.equal(tf.argmax(true_label, 1), tf.argmax(classifier_output, 1))
    accuracy_cls = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return loss_ae, loss_cls, accuracy_cls, train_op_ae, train_op_cls, classifier_output, dense, train_op, total_loss




