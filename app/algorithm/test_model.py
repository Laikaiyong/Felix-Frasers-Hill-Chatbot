from algo import FinalModel

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

model = FinalModel()

# X, y
X = model.X
y = model.y

# TF-IDF tokenize
tokenizer = Pipeline(
                [
                    ('vectoizer', CountVectorizer()), 
                    ('tfidf', TfidfTransformer())
                ]
            )
X = tokenizer.fit_transform(X).toarray()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# SVM evaluation
svm_model = SGDClassifier(
                loss='hinge', 
                penalty='l2',
                alpha=1e-3,
                max_iter=5, 
                tol=None
            ).fit(X_train, y_train)
svm_y_preds = svm_model.predict(X_test)
svm_score = svm_model.score(X_test, y_test)
svm_accuracy = accuracy_score(y_test, svm_y_preds)
svm_precision = precision_score(y_test, svm_y_preds, average='micro')
svm_recall = recall_score(y_test, svm_y_preds, average='micro')

model.print_metrics(
    "Support Vector Machine (SVM)",
    svm_score,
    svm_accuracy,
    svm_precision,
    svm_recall
    )

# Naive Bayes evaluation
nb_model = MultinomialNB().fit(X_train, y_train)
nb_y_preds = nb_model.predict(X_test)
nb_score = nb_model.score(X_test, y_test)
nb_accuracy = accuracy_score(y_test, nb_y_preds)
nb_precision = precision_score(y_test, nb_y_preds, average="micro")
nb_recall = recall_score(y_test, nb_y_preds, average="micro")

model.print_metrics(
    "Naive Bayes",
    nb_score,
    nb_accuracy,
    nb_precision,
    nb_recall
    )

# Decision Tree evaluation
dt_model = DecisionTreeClassifier().fit(X_train, y_train)
dt_y_preds = dt_model.predict(X_test)
dt_score = dt_model.score(X_test, y_test)
dt_accuracy = accuracy_score(y_test, dt_y_preds)
dt_precision = precision_score(y_test, dt_y_preds, average="micro")
dt_recall = recall_score(y_test, dt_y_preds, average="micro")

model.print_metrics(
    "Decision tree",
    dt_score,
    dt_accuracy,
    dt_precision,
    dt_recall
    )