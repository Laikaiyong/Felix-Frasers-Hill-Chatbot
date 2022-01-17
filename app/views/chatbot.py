from app.views import blueprint

from apu_cas import require_service_ticket, get_user_cas_attributes
from flask import render_template, request

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# http://127.0.0.1:5000/chatbot
@blueprint.route('/chatbot', methods=['GET'])
# @require_service_ticket
def get_role():
    # user_attribute = get_user_cas_attributes()
    # email = user_attribute.mail[0]
    # name = user_attribute.display_name[0]
    return render_template('chatbot.html')

@blueprint.route('/chatbot', methods=['POST'])
def add_role():
    message = request.form['message']
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(message)
    print(polarity)
    return render_template('chatbot.html')