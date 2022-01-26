from flask import Blueprint, render_template

blueprint = Blueprint('views', __name__)

# Route Declaration
from app.views import chatbot, plans

CONTENTS = [
    {
        "title":"Tourism Support ",
        "sub-title":"- Chat Conversation",
        "description":"Focus on Accommodations support and capable in responding User Intents on:",
        "items":[
          "Accomodations",
          "Greetings",
          "Travel Plan",
          "Place",
          "Activities Suggestion",
          "Goodbye"
        ],
        "img_url": "/static/img/chatbot-conversation.png"
    },
    {
        "title":"Built in ",
        "sub-title":"- Python",
        "description":"Developed dependents on python libraries:",
        "items":[
          "numpy",
          "pandas",
          "json",
          "scikit-learn",
          "nltk",
          "random"
        ],
        "img_url": "/static/img/python-image.png"
    },
    {
        "title":"With machine learning ",
        "sub-title":"algorithms",
        "description":"Built through AI algorithms such as:",
        "items":[
          "Count Vectorizer",
          "TF-IDF Vectorizer",
          "Support Vector Machine (SVM)",
          "Naive Bayes",
          "Decision Tree",
          "Ensemble Method"
        ],
        "img_url": "/static/img/wordcloud.png"
    }
]

MEMBERS = [
    {
        "image":"https://avatars.githubusercontent.com/u/76078213?v=4",
        "name":"Vandyck",
        "position":"Developer / Knowledge Base",
        "url": "https://www.linkedin.com/in/lai-kai-yong/"
    },
    {
        "image":"/static/img/Cheryl.jpg",
        "name":"Cheryl",
        "position":"Domain Expert / Knowledge Base",
        "url": "https://www.linkedin.com/in/lim-wye-yee-026717202" 
    },
    {
        "image":"/static/img/Cheong.jpg",
        "name":"Cheong",
        "position":"System Tester / Knowledge Base",
        "url": "https://www.linkedin.com/in/cheong-sheng-kui-263497224/" 
    },
    {
        "image":"/static/img/hk.jpeg",
        "name":"Hon Kit",
        "position":"System Analyst / Knowledge Base",
        "url": "https://www.linkedin.com/in/hon-kit-kok-0434b8211/" 
    }
]

@blueprint.route('/')
def index():
    return render_template(
                'index.html',
                contents=CONTENTS,
                members=MEMBERS
            )
    