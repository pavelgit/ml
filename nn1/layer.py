import numpy as np

class Layer: 
    def __init__(self, input_count, node_count):
        epsilon = 1e-1
        self.w = np.random.rand(node_count, input_count)*epsilon
        self.b = np.random.rand(node_count, 1)*epsilon
        self.z = np.zeros((node_count, 1))
        self.a = np.zeros((node_count, 1))
        self.dz_dinputs = None
        self.da_dz = None
        self.dj_dw = None
        self.dj_db = None
        self.inputs = None

    def propagate_forw(self, inputs):
        self.inputs = inputs
        self.z = self.w.dot(self.inputs) + self.b
        self.a = 1 / (1 + np.exp(-self.z))
        self.dz_dinputs = self.w.T
     
    def calculate_grads(self, dj_da):
        self.da_dz = self.a*(1-self.a)
        dj_dz = dj_da * self.da_dz
        
        dz_dw = self.inputs.T

        one_filled_array = np.zeros((1, dj_da.shape[1])).T
        one_filled_array.fill(1)
        dz_db = one_filled_array
        
        self.dj_dw = dj_dz.dot(dz_dw)
        self.dj_db = dj_dz.dot(dz_db)
     
    def apply_grads(self, learning_rate):
        self.w -= learning_rate * self.dj_dw
        self.b -= learning_rate * self.dj_db