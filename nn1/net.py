import numpy as np
from layer import Layer
import math

class Net:
 
    def __init__(self, input_count, layer_sizes, learning_rate=1e-1):
        self.learning_rate = learning_rate
        self.input_count = input_count
        self.layer_sizes = layer_sizes
        self.layer_count = len(layer_sizes)
        self.init_layers()
        
    def init_layers(self):
        self.layers = [
            Layer(self.input_count, self.layer_sizes[0])
        ]
        for i in range(1, self.layer_count): 
            layer = Layer(self.layer_sizes[i-1], self.layer_sizes[i])
            self.layers.append(layer)
            
        self.last_layer = self.layers[self.layer_count-1]

    def propagate_forw(self, examples):
        self.layers[0].propagate_forw(examples)
        for i in range(1, self.layer_count):
            self.layers[i].propagate_forw(self.layers[i-1].a)


    def propagate_forw_calc_cost(self, examples, labels):
        self.propagate_forw(examples)
        self.loss = -(labels * np.log(self.last_layer.a) + (1 - labels) * np.log(1 - self.last_layer.a))
        self.cost = np.sum(self.loss) / labels.shape[1]

    def calculate_grads(self, examples, labels): 
        x = examples
        y = labels
        
        dj_da = 1/y.shape[1] * (-y/self.last_layer.a + (1-y)/(1-self.last_layer.a))
        self.last_layer.calculate_grads(dj_da)

        for i in reversed(range(0, self.layer_count-1)):
            next_layer = self.layers[i+1]
            layer = self.layers[i]
            dj_da = next_layer.dz_dinputs.dot(dj_da * next_layer.da_dz)
            layer.calculate_grads(dj_da)

    def apply_grads(self):      
        for i in range(0, self.layer_count): 
            self.layers[i].apply_grads(self.learning_rate)

    def learn_once(self, examples, labels):
        self.propagate_forw_calc_cost(examples, labels)
        self.calculate_grads(examples, labels)
        self.apply_grads()

    def learn(self, examples, labels, epoch_count):
        for i in range(0, epoch_count):
            self.learn_once(examples, labels)
            if i % 1000 == 0:
                print(self.cost)

    def calc_error(self, examples, labels):
        example_count = examples.shape[1]
        result = self.predict(examples) > 0.5
        error = np.sum(np.abs(result-labels))/example_count
        return error

    def learn_minibatch(self, examples, labels, epoch_count, minibatch_size=256):
        example_count = examples.shape[1]
        full_minibatch_count = int(math.floor(example_count / minibatch_size))

        for i in range(0, epoch_count):
            for b in range(0, full_minibatch_count):
                minibatch = examples[:, b*minibatch_size:(b+1)*minibatch_size]
                minibatch_labels = labels[:, b*minibatch_size:(b+1)*minibatch_size]
                self.learn_once(minibatch, minibatch_labels)

            minibatch = examples[:, full_minibatch_count * minibatch_size:example_count]
            minibatch_labels = labels[:, full_minibatch_count * minibatch_size:example_count]
            self.learn_once(minibatch, minibatch_labels)

            if i % 1000 == 0:
                print(str(math.floor(i/epoch_count*100))+'% ', self.cost)

    def predict(self, examples):
        self.propagate_forw(examples)
        return self.last_layer.a