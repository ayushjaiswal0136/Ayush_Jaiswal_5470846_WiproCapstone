import os

class ConfigReader:

    @staticmethod
    def get(key):

        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "config.properties"
        )

        data = {}

        with open(path) as file:

            for line in file:

                if "=" in line:

                    k, v = line.strip().split("=")

                    data[k] = v

        return data.get(key)