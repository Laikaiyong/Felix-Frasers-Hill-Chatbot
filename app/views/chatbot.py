from app.views import blueprint
from app.algorithm import FinalModel

import json
import random
from itertools import chain

from apu_cas import require_service_ticket, get_user_cas_attributes
from flask import render_template, request

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

model = FinalModel()
X = model.X
y = model.y

messages_file = open('/Users/USER/Downloads/IAI/app/views/database/chatbot_init.json')
response_file = open('/Users/USER/Downloads/IAI/app/views/database/response.json')

messages = json.load(messages_file)['messages']
responses = json.load(response_file)

# http://127.0.0.1:5000/chatbot
@blueprint.route('/chatbot', methods=['GET'])
@require_service_ticket
def get_role():
    user_attribute = get_user_cas_attributes()
    email = user_attribute.mail[0]
    name = user_attribute.display_name[0]
    messages[0]['content'] = "Welcome {}, I am Vandyck chatbot, at your service.".format(name)
    return render_template('chatbot.html', messages=messages)

@blueprint.route('/chatbot', methods=['POST'])
def add_role():
    message = request.form['message']

    messages.append(
        {
            'sentBy': 'User',
            'content': message
        }
    )

    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(message)

    if polarity['neg'] > 0.5:
        messages.append({
            'sentBy': 'Bot',
            'content': 'Sorry your message is inappropriate. Mind your words.' 
        })
    else:
        X_train, input_message = model.tf_idf(message)
        svm_pred = model.svm(X_train, y, input_message)
        nb_pred = model.naive_bayes(X_train, y, input_message)
        dt_pred = model.decision_tree(X_train, y, input_message)
        predictions = list(chain(svm_pred, nb_pred, dt_pred))
        result = model.most_common_pred(predictions)

        # Callback Intent
        if not result:
            messages.append({
                'sentBy': 'Bot',
                'content': 'Sorry, I could not understand you.'
            })

            return render_template('chatbot.html', messages=messages)

        intentions = responses[result]
        random_response = random.choice(intentions)

        messages.append({
            'sentBy': 'Bot',
            'content': random_response
        })

    return render_template('chatbot.html', messages=messages)
