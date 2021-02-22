from InqsFileReader import InqsFileReader
from InqsNet import InqsNet
import traceback
import logging
from keras import optimizers

inqs_file_reader = InqsFileReader()

#inqs_file_reader.save_normalized(file_name='./data/inqs_orig.json', normalized_file_name='./data/inqs.json')
#exit(0)

inqs = inqs_file_reader.read(file_name='./data/inqs.json')
inputs_train, outputs_train, inputs_test, outputs_test = inqs_file_reader.get_arrays(inqs)

model = InqsNet().get_model(inputs_train[0].shape)
optimizer = optimizers.Adam(lr=0.001, decay=0.0001)
model.compile(optimizer=optimizer, loss='mean_absolute_percentage_error', metrics=['mean_absolute_percentage_error'])
model.fit(inputs_train, outputs_train, epochs=20, batch_size=16)
model.fit(inputs_train, outputs_train, epochs=20, batch_size=64)
model.fit(inputs_train, outputs_train, epochs=100, batch_size=256)
model.fit(inputs_train, outputs_train, epochs=100, batch_size=len(inputs_train))
evaluation_result = model.evaluate(inputs_test, outputs_test)

print()
print("Loss = " + str(evaluation_result[0]))
print("Test Accuracy = " + str(evaluation_result[1]))

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