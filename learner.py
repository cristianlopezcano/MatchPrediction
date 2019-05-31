from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

import ast
import math

HOME_WIN = 0
DRAW = 1
AWAY_WIN = 2

#Encodes 2 numbers as a pair
def pair(one, two):
    if one >= two:
        return one * one + one + two
    else:
        return two * two + one

print(tf.__version__)

f = open('training_data.txt')

raw_training_input = f.readlines()

f.close()

f = open('test_data.txt')

raw_test_input = f.readlines()

training_data = []
training_labels = []
home_goal_training_labels = []
away_goal_training_labels = []
score_training_labels = []
test_data = []
test_labels = []
home_goal_test_labels = []
away_goal_test_labels = []
score_test_labels = []

for line in raw_training_input:
    entry_list = ast.literal_eval(line)
    for entry in entry_list:
        entry = list(entry)
        training_data.append(entry[:24])
        training_labels.append(entry[24])
        if entry[25] > 4:
            home_goal_training_labels.append(4)
            p1 = 4
        else:
            home_goal_training_labels.append(entry[25])
            p1 = entry[25]
        if entry[26] > 4:
            away_goal_training_labels.append(4)
            p2 = 4
        else:
            away_goal_training_labels.append(entry[26])
            p2 = entry[26]
        score_training_labels.append(pair(p1,p2))

for line in raw_test_input:
    entry_list = ast.literal_eval(line)
    for entry in entry_list:
        entry = list(entry)
        test_data.append(entry[:24])
        test_labels.append(entry[24])
        if entry[25] > 4:
            home_goal_test_labels.append(4)
            p1 = 4
        else:
            home_goal_test_labels.append(entry[25])
            p1 = entry[25]
        if entry[26] > 4:
            away_goal_test_labels.append(4)
            p2 = 4
        else:
            away_goal_test_labels.append(entry[26])
            p2 = entry[26]
        score_test_labels.append(pair(p1,p2))

for count in range(len(training_data)):
    training_data[count] = np.asarray(training_data[count], dtype='int')
for count in range(len(test_data)):
    test_data[count] = np.asarray(test_data[count], dtype='int')
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
training_data = np.asarray(training_data, dtype='int')
test_data = np.asarray(test_data, dtype='int')
training_labels = np.asarray(training_labels, dtype='int')
test_labels = np.asarray(test_labels, dtype='int')
score_training_labels = np.asarray(score_training_labels, dtype='int')
score_test_labels = np.asarray(score_test_labels, dtype='int')

model = keras.Sequential([
  keras.layers.Dense(24, activation=tf.nn.selu),
  keras.layers.Dense(10, activation=tf.nn.tanh),
  keras.layers.Dense(5, activation=tf.nn.selu),
  keras.layers.Dense(5, activation=tf.nn.softmax)
])

score_model = keras.Sequential([
  keras.layers.Dense(24, activation=tf.nn.selu),
  keras.layers.Dense(40, activation=tf.nn.tanh),
  keras.layers.Dense(30, activation=tf.nn.selu),
  keras.layers.Dense(25, activation=tf.nn.softmax)
])

model.compile(optimizer='SGD',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(training_data, training_labels, epochs=10)

test_loss,test_acc = model.evaluate(test_data, test_labels)

predictions = model.predict(test_data)

model.fit(training_data, home_goal_training_labels, epochs=5)

test_loss,home_test_acc = model.evaluate(test_data, home_goal_test_labels)


model.fit(training_data, away_goal_training_labels, epochs=5)

test_loss,away_test_acc = model.evaluate(test_data, away_goal_test_labels)

score_model.compile(optimizer='SGD',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

score_model.fit(training_data, score_training_labels, epochs=10)

score_loss,score_acc = score_model.evaluate(test_data, score_test_labels)

print("Test accuracy: ", test_acc)

print("Home goal test accuracy: ", home_test_acc)

print("Away goal test accuracy: ", away_test_acc)

print("Correct score accuracy: ", score_acc)

average_gain = 1
competitor_gain = 1
for count in range(len(predictions)):
    average_gain *= predictions[count][test_labels[count]]
    average_gain = math.sqrt(average_gain)
    competitor_gain *= 1 / ((test_data[count][18 + test_labels[count]]) / 100)
    competitor_gain = math.sqrt(competitor_gain)


print("Average prediction gain: "  + str(average_gain))
print("Average competitor gain: " + str(competitor_gain))

total_gain = 0
amount_bet = 0
lowest_balance = 0
lowest_balance_point = 0
for count in range(len(predictions)):
    home_win_prob = predictions[count][0]
    draw_prob = predictions[count][1]
    away_win_prob = predictions[count][2]
    home_win_odds = test_data[count][18] / 100
    draw_odds = test_data[count][19] / 100
    away_win_odds = test_data[count][20] / 100
    home_win_gain = home_win_prob * home_win_odds
    draw_gain = draw_prob * draw_odds
    away_win_gain = away_win_prob * away_win_odds
    actual_result = test_labels[count]

    if home_win_gain > 1.2:
        bet_size = home_win_gain * 100
        total_gain -= bet_size
        amount_bet += bet_size
        if total_gain < lowest_balance:
            lowest_balance = total_gain
            lowest_balance_point = count
        if actual_result == HOME_WIN:
            total_gain += bet_size * home_win_odds


    if draw_gain > 1.2:
        bet_size = draw_gain * 100
        amount_bet += bet_size
        total_gain -= bet_size
        if total_gain < lowest_balance:
            lowest_balance = total_gain
            lowest_balance_point = count
        if actual_result == DRAW:
            total_gain += bet_size * draw_odds

    if away_win_gain > 1.2:
        bet_size = away_win_gain * 100
        amount_bet += bet_size
        total_gain -= bet_size
        if total_gain < lowest_balance:
            lowest_balance = total_gain
            lowest_balance_point = count
        if actual_result == AWAY_WIN:
            total_gain += bet_size * away_win_odds



print("The total amount bet was " + str(amount_bet))
print("The lowest acheived balance was " + str(lowest_balance) + " on iteration " +  \
         str(lowest_balance_point) + "/" + str(len(predictions)))
print("The total gain from bet365 was " + str(total_gain))
