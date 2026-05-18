import csv
import os

class CSVReader:

    @staticmethod
    def read_csv(file_name):

        data = []

        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            file_name
        )

        with open(path) as file:

            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

        return data