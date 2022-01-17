import numpy as np
import pandas as pd

import json
import string
from collections import Counter
from itertools import chain

from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Self coded algorithm
class SelfModel:
    def __init__(self):
        self.data = self._get_data()['data']
        self.X = self._get_data()['X']
        self.y = self._get_data()['y']
        self.unique_X = self._get_data()['unique_X']
        self.unique_y = self._get_data()['unique_y']

    # Training Data
    def _get_data(self):
        # Read data and process
        unprocessed_data = pd.read_excel('data.xlsx')

        # X, y
        X = unprocessed_data['message'].tolist()
        y = unprocessed_data['intent'].tolist()
        unique_X = np.unique(X)
        unique_y = np.unique(y)

        return {
            "data": unprocessed_data,
            'X': X,
            'y': y,
            'unique_X': unique_X,
            'unique_y': unique_y
        }

    # Bag of words algorithm (*Getting a glimpse on the algorithm)
    def bag_of_words(*args):
        # Lowercase
        original_words = args[0]
        lower_words = np.char.lower(original_words).tolist()

        # Remove punctuation
        punc_format = str.maketrans('', '', string.punctuation)
        removed_punc = np.array([word.translate(punc_format) for word in lower_words])

        # Split words
        split_words = np.char.split(removed_punc).tolist()

        # Stop words Removal
        unwanted = stopwords.words("english")
        removed_sw = np.array([word for word in split_words if word not in unwanted]).tolist()

        print(removed_sw)

        # Negation handling (* Might not perform tis due to lost of meaning)

        # Frequency
        frequency_list = []
        for removed in removed_sw:
            frequency_list.append(dict(Counter(removed)))
        
        print(frequency_list)

        return frequency_list
    
    def nlp_process(self):
        pass

# TensorFlow + Scikitlearn dependency algorithm
class FinalModel(SelfModel):
    # Bag of words algorithm 
    # (ps: tis algo performs all the following steps from the parent + negation)
    def bag_of_words(*args):
        # Count Vectorizer initialization
        count_vector = CountVectorizer(stop_words='english').fit(args[0])

        # Dataframe for frequency
        frequency_list = count_vector.transform(args[0]).toarray()
        features_name = count_vector.get_feature_names_out()

        frequency_matrix = pd.DataFrame(frequency_list, columns=features_name)

        print(frequency_matrix)
        return frequency_matrix

SelfModel.bag_of_words(SelfModel().X)