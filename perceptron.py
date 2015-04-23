import random

from matplotlib.pyplot import plot, show
from scipy.linalg import norm

from numpy.testing import rand


LEARNING_RATE = 0.5

GENERATED_DATA_AMOUNT = 50

ITERATION_MAX = 100


class Perceptron:
    def __init__(self, inputs_number):
        self.weights = []
        for index in range(inputs_number):
            self.weights.append(random.random())
        # self.weights = [random.random(), random.random(), random.random()]  # depends on amount of inputs
        self.learning_rate = LEARNING_RATE  # learning speed
        self.train(generate_data(GENERATED_DATA_AMOUNT))

    def activation(self, inputs_row):
        # dot product calc

        rez = self.weights[0] * inputs_row[0] + \
              self.weights[1] * inputs_row[1] + \
              self.weights[2] * inputs_row[2]
        if rez >= 0:
            return 1
        else:
            return 0

    def train(self, training_data):
        learned = False
        iteration = 0
        while not learned:
            global_error = 0.0
            for row in training_data:  # for each sample
                response = self.activation(row)
                if row[-1] != response:  # if we have a wrong response
                    iter_error = row[-1] - response  # desired response - actual response
                    self.update_weights(row, iter_error)
                    global_error += abs(iter_error)  # absolute value
            iteration += 1
            if global_error == 0 or iteration >= ITERATION_MAX:  # over fitting
                learned = True  # stop learning

    def update_weights(self, training_data_row, iter_error):
        self.weights[0] += self.learning_rate * iter_error * training_data_row[0]
        self.weights[1] += self.learning_rate * iter_error * training_data_row[1]
        self.weights[2] -= self.learning_rate * iter_error


def generate_data(n):
    xb = (rand(n) * 2 - 1) / 2 - 0.5
    yb = (rand(n) * 2 - 1) / 2 + 0.5
    xr = (rand(n) * 2 - 1) / 2 + 0.5
    yr = (rand(n) * 2 - 1) / 2 - 0.5
    inputs = []
    for i in range(len(xb)):
        inputs.append([xb[i], yb[i], -1, 1])  # threshold -1
        inputs.append([xr[i], yr[i], -1, 0])
    return inputs

# Creating a perceptron object:


perceptron = Perceptron(3)  # perceptron instance

test_set = generate_data(100)  # test set generation

# Perceptron test
for row in test_set:
    response = perceptron.activation(row)
    if response != row[-1]:  # if the response is not correct
        print('error')

    if response == 1:
        plot(row[0], row[1], 'ob')
    else:
        plot(row[0], row[1], 'og')

# plot of the separation line.
# The separation line is orthogonal to w
vector_length = norm(perceptron.weights)
normalized_vector_arr = []
for weight in perceptron.weights:
    normalized_vector_arr.append(weight / vector_length)

orthogonal_up = [normalized_vector_arr[1], -normalized_vector_arr[0]]
orthogonal_down = [-normalized_vector_arr[1], normalized_vector_arr[0]]
plot([orthogonal_up[0], orthogonal_down[0]], [orthogonal_up[1], orthogonal_down[1]], '--k')
show()