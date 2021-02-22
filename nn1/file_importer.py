import pandas as pd

class FileImporter:

    def import_file(self):
        csv_data = pd.read_csv("/home/pavel/work/ml/AAPL.csv")
        csv_data_array = csv_data.as_matrix()
        data = list(map(lambda r: { 'date': r[0], 'open': r[1], 'high': r[2], 'low': r[3], 'close': r[4] }, csv_data_array))
        return data