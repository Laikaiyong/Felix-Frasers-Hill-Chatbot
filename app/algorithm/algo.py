import numpy as np
import pandas as pd

import os
import math
import json
import string
from collections import Counter
from itertools import chain

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier


import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer # Might not use data stemming

nltk.download('stopwords')
nltk.download('vader_lexicon')

dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, 'database/data.xlsx')

# Self coded algorithm
class SelfModel:
    def __init__(self):
        self.data = self._get_data()['data']
        self.X = self._get_data()['X']
        self.y = self._get_data()['y']
        self.unique_y = self._get_data()['unique_y']

    # Training Data
    def _get_data(self):
        # TODO: Change excel File location based on your directory
        # Read data and process
        excel_data = pd.ExcelFile(data_path)
        unprocessed_data = pd.read_excel(excel_data, 'Data')

        # X, y
        X = unprocessed_data['message'].values.astype('U')
        y = unprocessed_data['intent']

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

    # BoW algo (getting a glimpse on the algorithm)
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
        counter = [dict(Counter(removed)) for removed in removed_sw]
        unique_features = [
                            [
                                key
                                for key in list(
                                    dictionary.keys()
                                )
                            ]
                            for dictionary in counter
                          ]
        flatten_features = list(np.unique(np.concatenate(unique_features).flat))

        frequency_list = []
        for i in range(len(list_items)):
            frequency_item = []
            for key, value in counter[i].items():
                frequency_object = []
                for feature in flatten_features:
                    if key == feature:
                        frequency_object.append(value)
                        continue
                    else:
                        frequency_object.append(0)
                frequency_item.append(frequency_object)
            frequency_list.append(np.sum(np.array(frequency_item), axis=0))

        return {
            'frequency_list': frequency_list,
            'features': flatten_features
        }
    
    # Just getting a glimpse on algorithm
    def tf_idf(self,data_array):
        tf = self.bag_of_words(data_array)['frequency_list']
        features = self.bag_of_words(data_array)['features']

        """"
        TODO: There are some error in the calculation 
        """
        # broadcasting data into 1d array
        row = np.sum(np.array(tf), axis=1).tolist()
        column = np.sum(np.array(tf), axis = 0).tolist()

        # Calculate idf
        idf = []
        for col in column:
            idf.append(math.log10(len(data_array)/col))

        # Multiply tf & idf
        tf_idf_array = []
        for freq_row in range(len(tf)):
            tf_idf_row = []
            for freq_col in range(len(tf[freq_row])):
                if row[freq_row] != 0:
                    tf_idf_row.append(idf[freq_col] * (tf[freq_row][freq_col]/row[freq_row]))
                else:
                    tf_idf_row.append(0)
            tf_idf_array.append(tf_idf_row)
        
        return tf_idf_array

    def _recreate_sentence(self, text):
        sentence =" ".join(text)
        return sentence

    
    def clean_input(self, message):
        lower_msg = self._lowercase_word(message)
        no_punc_msg = self._remove_punctuation(lower_msg)
        splitted_msg = self._split_word(no_punc_msg)
        no_sw_msg = self._stop_word_removal(splitted_msg)
        sentence = self._recreate_sentence(no_sw_msg)
        return sentence
    
    def print_metrics(self, name, model_score, accuracy, precision, recall):
        print(
            f"""
            Model Name: {name}
            Model Score: {model_score}
            Accuracy Score: {accuracy}
            Precision Score: {precision}
            Recall Score: {recall}
            """
        )
    
# TensorFlow + Scikitlearn dependency algorithm
class FinalModel(SelfModel):
    def __init__(self):
        SelfModel.__init__(self)
        self.tf_idf_model = Pipeline(
                                [
                                    ('vectoizer', CountVectorizer()), 
                                    ('tfidf', TfidfTransformer())
                                ]
                            )
        self.svm_model = SGDClassifier(
                            loss='hinge', penalty='l2',
                            alpha=1e-3, random_state=42,
                            max_iter=5, tol=None
                          )
        
        self.naive_bayes_model = MultinomialNB()
        self.tree_model = DecisionTreeClassifier()

    def bag_of_words(*args):
        """
        Bag of words algorithm 
        (ps: tis function performs all the data cleaning and count the frequency of)
        """
        # Count Vectorizer initialization
        count_vector = CountVectorizer(stop_words='english').fit(args[0])

        # Dataframe for frequency
        frequency_list = count_vector.transform(args[0]).toarray()
        features_name = count_vector.get_feature_names_out()

        # frequency_matrix = pd.DataFrame(frequency_list, columns=features_name)

        return {
            'frq_list': frequency_list
        }

    def tf_idf(self, message):
        X_train = self.tf_idf_model.fit_transform(self.X).toarray()
        input_words = self.tf_idf_model.transform([self.clean_input(message)])
        return X_train, input_words

    # Support Vector Machine (SVM)
    def svm(self, train_data, y, input_words):
        svm_model = self.svm_model.fit(train_data, y)
        svm_pred = svm_model.predict(input_words)
        print("SVM ", svm_pred)

        return svm_pred
    
    # Naive bayes multinomial 
    def naive_bayes(self, train_data, y, input_words):
        nb_model = self.naive_bayes_model.fit(train_data, y)
        nb_pred = nb_model.predict(input_words)
        print("NB ", nb_pred)

        return nb_pred

    # Decision Tree
    def decision_tree(self, train_data, y, input_words):
        dt_model = self.tree_model.fit(train_data, y)
        dt_pred = dt_model.predict(input_words)
        print("DT ", dt_pred)

        return dt_pred
    
    def most_common_pred(self, pred_list):
        unique_pred = set(pred_list)
        if len(unique_pred) == 3:
            return pred_list[0]
        return max(unique_pred, key=pred_list.count)

# Example Usage + Prediction
hi = FinalModel()
X = hi.X
y = hi.y
X_train, input_message = hi.tf_idf("bye")
svm_pred = hi.svm(X_train, y, input_message)
# print(svm_pred)
nb_pred = hi.naive_bayes(X_train, y, input_message)
# print(nb_pred)
dt_pred = hi.decision_tree(X_train, y, input_message)
# print(dt_pred)
predictions = list(chain(svm_pred, nb_pred, dt_pred))
result = hi.most_common_pred(predictions)

# print(result)
