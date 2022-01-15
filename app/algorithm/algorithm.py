import numpy as np
import pandas as pd

class Algorithm:
    def __init__(self, x, y):
        self.data = self.get_data()
        self.x = x
        self.y = y

    def get_data(self):
        unprocessed_data = pd.read_excel('data.xlsx')
        self.data = unprocessed_data
        return self.data

    def nlp_process(self):
        pass

new_algo = Algorithm()
print(new_algo.data)