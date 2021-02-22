import json
import numpy as np

class InqsFileReader:

    def read(self, inputs_file_name, outputs_file_name, dev_length = 200):
        inputs = json.load(open(inputs_file_name))
        outputs = json.load(open(outputs_file_name))
        return self.get_sets(inputs, outputs, dev_length)

    def get_sets(self, inputs, outputs, dev_length):
        np.random.seed(123)

        length = len(inputs)

        shuffled_inputs = list(inputs)
        np.random.shuffle(shuffled_inputs)
        shuffled_outputs = list(outputs)
        np.random.shuffle(shuffled_outputs)

        inputs_split = np.split(np.array(shuffled_inputs), [length - dev_length])
        outputs_split = np.split(np.array(shuffled_outputs), [length - dev_length])

        inputs_train = inputs_split[0]
        inputs_test = inputs_split[1]

        outputs_train = outputs_split[0]
        outputs_test = outputs_split[1]

        return inputs_train, outputs_train, inputs_test, outputs_test

    def read_arrays_from_prompt(self):
        text = input()
        inq = json.loads(text)
        normalized_inq = self.normalize_inq(inq)
        input_array, output_array = self.map_inq_to_arrays(normalized_inq)
        return np.array([input_array]), np.array([output_array])

