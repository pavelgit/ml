from keras.layers import Input, Dense, Activation, BatchNormalization, Dropout
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Model

class InqsNet:

    def get_model(self, input_shape):
        x_input = Input(input_shape)

        x = x_input

        x = Dense(4, activation='relu')(x)

        # x = BatchNormalization()(x)
        # x = Dense(1000, activation='tanh')(x)
        # x = BatchNormalization()(x)
        # x = Dense(1000, activation='tanh')(x)
        # x = BatchNormalization()(x)
        # x = Dense(500, activation='tanh')(x)
        # x = BatchNormalization()(x)
        # x = Dense(50, activation='relu')(x)

        x = Dense(1, activation='relu')(x)

        model = Model(inputs=x_input, outputs=x)

        return model