from net import Net
from set_generator import SetGenerator
import numpy as np
from plot import Plot

def main1():

    (examplesArray, labelsArray) = SetGenerator().generate_linear()
    examples = np.array(examplesArray).T
    labels = np.array([labelsArray])
    net = Net(2, [1])
    net.learn(examples, labels, 10000)
    Plot().plot(net, examples, labels)

    input("Press Enter to continue...")

def main2():

    (examplesArray, labelsArray) = SetGenerator().generate_circle_2(1000)
    examples = np.array(examplesArray).T
    labels = np.array([labelsArray])
    examples_dev = examples[:, 0:900]
    labels_dev = labels[:, 0:900]
    examples_test = examples[:, 900:1000]
    labels_test = labels[:, 900:1000]

    net = Net(2, [10, 1], learning_rate=10)
    net.learn_minibatch(examples_dev, labels_dev, 2000, minibatch_size=32)
    print('error:', net.calc_error(examples_test, labels_test))
    Plot().plot(net, examples, labels)

    input("Press Enter to continue...")

main2()
