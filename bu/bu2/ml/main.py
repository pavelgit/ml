from InqsFileReader import InqsFileReader
from InqsNet import InqsNet
import traceback
import logging
from keras import optimizers
import numpy as np

inqs_file_reader = InqsFileReader()

inputs_train, outputs_train, inputs_test, outputs_test = \
    inqs_file_reader.read('./data/input.json', './data/output.json', dev_length=200)

inputs_train = np.array([[1., 0.], [1., 1.], [0., 1.], [2., 3.]], dtype=np.float32)
outputs_train = np.array([[3.], [6.], [3.], [15.]], dtype=np.float32)

model = InqsNet().get_model(inputs_train[0].shape)
optimizer = optimizers.Adam(lr=1, decay=0.0001)
model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mean_absolute_error'])
model.fit(inputs_train, outputs_train, epochs=10000, batch_size=len(inputs_train))
evaluation_result = model.evaluate(inputs_test, outputs_test)

print()
print("binary_crossentropy loss = " + str(evaluation_result[0]))
print("mean_absolute_error = " + str(evaluation_result[1]))

exit(0)

while True:
    try:
        input_array, output_array = inqs_file_reader.read_arrays_from_prompt()
        print(model.predict(input_array))
        evaluation_result = model.evaluate(input_array, output_array)
        print()
        print("Loss = " + str(evaluation_result[0]))
        print("Test Accuracy = " + str(evaluation_result[1]))

    except Exception as e:
        logging.error(traceback.format_exc())


pass