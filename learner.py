from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

import ast

HOME_WIN = 0
DRAW = 1
AWAY_WIN = 2

print(tf.__version__)

f = open('training_data.txt')

raw_training_input = f.readlines()

f.close()

f = open('test_data.txt')

raw_test_input = f.readlines()

training_data = []
training_labels = []
test_data = []
test_labels = []

for line in raw_training_input:
    entry_list = ast.literal_eval(line)
    for entry in entry_list:
        entry = list(entry)
        training_data.append(entry[:18])
        training_labels.append(entry[18])

for line in raw_test_input:
    entry_list = ast.literal_eval(line)
    for entry in entry_list:
        entry = list(entry)
        test_data.append(entry[:18])
        test_labels.append(entry[18])

for count in range(len(training_data)):
    training_data[count] = np.asarray(training_data[count])
for count in range(len(test_data)):
    test_data[count] = np.asarray(test_data[count])
for count in range(len(training_labels)):
    if training_labels[count] == 'H':
        training_labels[count] = HOME_WIN
    elif training_labels[count] == 'D':
        training_labels[count] = DRAW
    elif training_labels[count] == 'A':
        training_labels[count] = AWAY_WIN
for count in range(len(test_labels)):
    if test_labels[count] == 'H':
        test_labels[count] = HOME_WIN
    elif test_labels[count] == 'D':
        test_labels[count] = DRAW
    elif test_labels[count] == 'A':
        test_labels[count] = AWAY_WIN
training_data = np.asarray(training_data)
test_data = np.asarray(test_data)
training_labels = np.asarray(training_labels)
test_labels = np.asarray(test_labels)

print(training_data)
model = keras.Sequential([
  keras.layers.Flatten(input_shape=(18,)),
  keras.layers.Dense(128, activation=tf.nn.relu),
  keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(training_data, training_labels, epochs=5)

test_loss,test_acc = model.evaluate(test_data, test_labels)

print("Test accuracy: ", test_acc)
