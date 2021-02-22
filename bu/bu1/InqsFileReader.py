import json
import dateutil.parser
from datetime import date
import numpy as np
from keras.utils import np_utils
from mapping.professional_training_mapping import professional_training_mapping
from mapping.salutation_mapping import salutation_mapping
from mapping.smoker_mapping import smoker_mapping
from mapping.def_prof_training_mapping import def_prof_training_mapping
from mapping.education_status_mapping import education_status_mapping
from mapping.occupation_id_mapping import occupation_id_mapping
from mapping.occupation_status_mapping import occupation_status_mapping

class InqsFileReader:

    def read(self, file_name='inqs.json'):
        return json.load(open(file_name))

    def normalize_inq(self, inq):
        normalized_inq = {}
        birthday = dateutil.parser.parse(inq['birthday'])

        normalized_inq['salutation'] = str(inq['salutation'])
        normalized_inq['professionalTraining'] = str(inq['professionalTraining'])
        normalized_inq['smoker'] = str(inq['smoker'])
        normalized_inq['definitionProfessionalTraining'] = str(inq['definitionProfessionalTraining'])
        normalized_inq['educationStatus'] = str(inq['educationStatus'])
        normalized_inq['occupationId'] = str(inq['occupationId'])
        normalized_inq['fractionHardWork'] = float(inq['fractionHardWork'])
        normalized_inq['fractionOfficeWork'] = float(inq['fractionOfficeWork'])
        normalized_inq['staffResponsibility'] = float(inq['staffResponsibility'])
        normalized_inq['occupationStatus'] = str(inq['occupationStatus'])
        normalized_inq['age'] = float(self.get_age(birthday))
        normalized_inq['benefitAmount'] = float(inq['benefitAmount'])
        normalized_inq['benefitAgeLimit'] = float(inq['benefitAgeLimit'])
        normalized_inq['bruttoPrice'] = float(inq['bruttoPrice'])
        normalized_inq['nettoPrice'] = float(inq['nettoPrice'])

        return normalized_inq

    def normalize(self, inqs):
        normalized_inqs = []
        for inq in inqs:
            normalized_inqs.append(self.normalize_inq(inq))

        return normalized_inqs

    def save_normalized(self, file_name='inqs.json', normalized_file_name='normalized_inqs.json'):
        normalized_inqs = self.normalize(self.read(file_name))
        with open(normalized_file_name, 'w') as outfile:
            json.dump(normalized_inqs, outfile)

    def get_age(self, birthday):
        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def one_hot(self, value, mapping):
        return np_utils.to_categorical(mapping[value], len(mapping))

    def map_inq_to_arrays(self, inq):
        salutation_oh = self.one_hot(inq['salutation'], salutation_mapping)
        professional_training_oh = self.one_hot(inq['professionalTraining'], professional_training_mapping)
        smoker_oh = self.one_hot(inq['smoker'], smoker_mapping)
        def_prof_training_oh = self.one_hot(inq['definitionProfessionalTraining'], def_prof_training_mapping)
        education_status_oh = self.one_hot(inq['educationStatus'], education_status_mapping)
        occupation_id_oh = self.one_hot(inq['occupationId'], occupation_id_mapping)
        occupation_status_oh = self.one_hot(inq['occupationStatus'], occupation_status_mapping)

        input_array = []
        input_array.extend(salutation_oh)
        input_array.extend(professional_training_oh)
        input_array.extend(smoker_oh)
        input_array.extend(def_prof_training_oh)
        input_array.extend(education_status_oh)
        input_array.extend(occupation_id_oh)
        input_array.extend(occupation_status_oh)

        input_array.append(inq['fractionHardWork'])
        input_array.append(inq['fractionOfficeWork'])
        input_array.append(inq['staffResponsibility'])
        input_array.append(inq['age'])
        input_array.append(inq['benefitAmount'])
        input_array.append(inq['benefitAgeLimit'])

        output_array = [
            inq['bruttoPrice'],
            inq['nettoPrice']
        ]

        return input_array, output_array


    def get_arrays(self, inqs):
        np.random.seed(123)
        shuffled_inqs = list(inqs)
        np.random.shuffle(shuffled_inqs)

        length = len(shuffled_inqs)
        inputs = []
        outputs = []

        for inq in shuffled_inqs:
            input_array, output_array = self.map_inq_to_arrays(inq)

            inputs.append(input_array)
            outputs.append(output_array)

        dev_length = 200
        inputs_split = np.split(np.array(inputs), [length - dev_length])
        outputs_split = np.split(np.array(outputs), [length - dev_length])

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

