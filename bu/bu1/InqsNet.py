from keras.layers import Input, Dense, Activation, BatchNormalization
from keras.models import Model

class InqsNet:

    def get_model(self, input_shape):
        x_input = Input(input_shape)

        x = x_input

        x = Dense(1000, activation='relu', name='dense1')(x)
        x = BatchNormalization(axis=1, name='bn2')(x)
        x = Dense(1000, activation='relu', name='dense3')(x)
        x = BatchNormalization(axis=1, name='bn3')(x)
        x = Dense(1000, activation='relu', name='dense4')(x)
        x = BatchNormalization(axis=1, name='bn4')(x)
        x = Dense(100, activation='relu', name='dense5')(x)
        x = BatchNormalization(axis=1, name='bn5')(x)
        x = Dense(20, activation='relu', name='dense6')(x)
        x = BatchNormalization(axis=1, name='bn6')(x)

        #x = BatchNormalization(axis=1, name='bn1')(x)
        #x = Activation('relu')(x)

        #x = Dense(1000, activation='relu', name='dense2')(x)

        #x = BatchNormalization(axis=1, name='bn2')(x)
        #x = Activation('relu')(x)

        x = Dense(2, activation='relu', name='dense_output')(x)

        model = Model(inputs=x_input, outputs=x, name='InqsNet')

        return model