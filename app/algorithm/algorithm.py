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
        self.unique_y = self._get_data()['unique_y']

    # Training Data
    def _get_data(self):
        # Read data and process
        unprocessed_data = pd.read_excel('data.xlsx')

        # X, y
        X = unprocessed_data['message'].tolist()
        y = unprocessed_data['intent'].tolist()
        unique_y = np.unique(y)

        return {
            "data": unprocessed_data,
            'X': X,
            'y': y,
            'unique_y': unique_y
        }

    
    def _lowercase_word(self, words):
        messages = words
        if isinstance(messages, list) or isinstance(messages, tuple):
            return np.char.lower(messages).tolist()
        else:
            return messages.lower()
    
    def _remove_punctuation(self, words):
        punc_format = str.maketrans('', '', string.punctuation)
        if isinstance(words, list) or isinstance(words, tuple):
            return np.array([word.translate(punc_format) for word in words]).tolist()
        else:
            return words.translate(punc_format)
    
    def _split_word(self, words):
        if isinstance(words, list) or isinstance(words, tuple):
            return np.char.split(words).tolist()
        else:
            return words.split()

    def _stop_word_removal(self, words):
        unwanted = stopwords.words("english")
        return np.array([word for word in words if word not in unwanted], dtype=object).tolist()

    # Bag of words algorithm (*Getting a glimpse on the algorithm)
    def bag_of_words(self, list_items):
        # Lowercase
        original_words = list_items
        lower_words = self._lowercase_word(original_words)

        # Remove punctuation
        removed_punc = self._remove_punctuation(lower_words)

        # Split words
        splitted = self._split_word(removed_punc)

        # Stop words Removal
        removed_sw = self._stop_word_removal(splitted)

        # Negation handling (* Might not perform tis due to lost of meaning)

        # Frequency
        frequency_list = []
        for removed in removed_sw:
            frequency_list.append(dict(Counter(removed)))

        return frequency_list
    
    def clean_input(self, message):
        lower_msg = self._lowercase_word(message)
        no_punc_msg = self._remove_punctuation(lower_msg)
        splitted_msg = self._split_word(no_punc_msg)
        no_sw_msg = self._stop_word_removal(splitted_msg)
        return no_sw_msg


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
        return {
            'frq_list': frequency_list
        }
    
    def naive_bayes(self):
        pass

hey = SelfModel()
hey.bag_of_words(hey.X)
print(hey.clean_input('Hi nice to meet you.'))