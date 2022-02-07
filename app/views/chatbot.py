from app.views import blueprint
from app.algorithm import FinalModel
from app.maps import location_url

import re
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

HOTELS = [
    "Shahzan Inn",
    "Puncak Inn",
    "The Pines",
    "Silverpark Resort",
    "Green Acres"
]

GENERAL = [
    "greetings",
    "thankyou",
    "goodbye",
    "activities",
    "suggestplan",
    "funfacts",
    "location",
    "fees",
    "prepare",
    "ac_restaurant"
]

AC_RELATED = [
    "ac_roomtype",
    "ac_facilities",
    "ac_review",
    "ac_fnb_onsite"
]

AC_HOTEL_IMAGES = {
    "Shahzan Inn": 
            "https://www.shahzaninn-fraserhill.com/wp-content/uploads/2019/07/shahzan_inn_2019.jpg",
        "Puncak Inn": 
            "https://www.pahangtourism.org.my/media/k2/items/cache/5a61d31ed794cb758475f6c89477dfed_XL.jpg?t=1517199358",
        "The Pines":
            "https://pix10.agoda.net/hotelImages/190/19019783/19019783_20110615360093162641.jpg?s=1024x768",
        "Silverpark Resort": 
            "https://www.fraserhill.info/img/frasers-silverpark-resort-entrance.jpg",
        "Green Acres": 
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/236464932.jpg?k=25717e35db0795538c371cac3a9f8528d8cf728766679cb29bd986bf41c7fa33&o=&hp=1"
}

AC_URL = {
    "Shahzan Inn":
        "https://www.shahzaninn-fraserhill.com/",
    "Puncak Inn":
        "https://www.puncakinn.com/",
    "The Pines":
        "https://www.thepines.com.my/main.htm",
    "Silverpark Resort":
        "http://www.silverparkresort.com/",
    "Green Acres":
        "https://www.greenacresfraser.com/"
}

AC_BOOK_URL = {
    "Shahzan Inn":
        "https://www.shahzaninn-fraserhill.com/",
    "Puncak Inn":
        "http://www.puncakinn.pkbf.gov.my/",
    "The Pines":
        "https://www.agoda.com/the-pines-resort-fraser-s-hill-malaysia/hotel/kuala-lumpur-my.html?cid=1844104&checkIn=2022-01-27&los=1&travellerType=1",
    "Silverpark Resort":
        "https://www.tripadvisor.com.my/Hotel_Review-g303992-d1135358-Reviews-Fraser_s_Silverpark_Resort-Bukit_Fraser_Raub_District_Pahang.html",
    "Green Acres":
        "https://www.greenacresfraser.com/fraserhill"
}

messages_file = open('/Users/USER/Downloads/IAI/app/views/database/chatbot_init.json')
response_file = open('/Users/USER/Downloads/IAI/app/views/database/response.json')

messages = json.load(messages_file)['messages']
responses = json.load(response_file)

response_file.close()

# http://127.0.0.1:5000/chatbot
@blueprint.route('/chatbot', methods=['GET'])
@require_service_ticket
def get_role():
    user_attribute = get_user_cas_attributes()
    email = user_attribute.mail[0]
    name = user_attribute.display_name[0]
    with open('/Users/USER/Downloads/IAI/app/views/database/tag.txt', 'w') as init:
        init.write('')
    messages[0]['content'] = "Welcome {}, I am Felix chatbot, at your service.".format(name)
    return render_template('chatbot.html', messages=messages)

@blueprint.route('/chatbot', methods=['POST'])
def add_role():
    tag_file = open('/Users/USER/Downloads/IAI/app/views/database/tag.txt')
    accomodation_tag = tag_file.read()
    tag_file.close()

    message = request.form['message']

    messages.append(
        {
            'sentBy': 'User',
            'content': message,
            'tag': ''
        }
    )

    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(message)

    if polarity['neg'] > 0.5:
        messages.append({
            'sentBy': 'Bot',
            'content': 'Sorry your message is inappropriate. Mind your words.' 
        })

        return render_template(
                'chatbot.html', 
                messages=messages
            )
    
    if message in HOTELS:
        with open('/Users/USER/Downloads/IAI/app/views/database/tag.txt', 'w') as get_tag:
            get_tag.write(message)
        
        accomodation_tag = message
        messages.append({
            'sentBy': 'Bot',
            'content': responses["ac_info"][accomodation_tag]
        })

        return render_template(
                'chatbot.html', 
                messages=messages
            )       

    X_train, input_message = model.tf_idf(message)
    svm_pred = model.svm(X_train, y, input_message)
    nb_pred = model.naive_bayes(X_train, y, input_message)
    dt_pred = model.decision_tree(X_train, y, input_message)
    predictions = list(chain(svm_pred, nb_pred, dt_pred))
    result = model.most_common_pred(predictions)

    if message == "Onsite":
        result = 'ac_fnb_onsite'
    elif message == "Offsite":
        result = "ac_fnb_offsite"
    elif re.sub(r'[^\w\s]', '', message.lower()) in ['where', 'where is it', 'where is the hotel', 'where is the homestay', 'where is the resort']:
        result = 'ac_location'

    # Accomodations
    if result == 'accommodation':
        options = HOTELS
        messages.append({
            'sentBy': 'Bot',
            'content': responses[result]
        })

        return render_template(
                'chatbot.html', 
                messages=messages,
                options=options
            )

    if accomodation_tag and result not in AC_RELATED and result not in [item for item in GENERAL if item not in ['fees', 'location']]:
        match [result]:

            case [('ac_location' | 'location')]:
                messages.append({
                    'sentBy': 'Bot',
                    'content': responses['ac_location'],
                    'url': location_url(accomodation_tag)
                })

            case [('ac_price' | 'fees')]:
                messages.append({
                    'sentBy': 'Bot',
                    'content': responses['ac_price'][accomodation_tag]
                })

            case ['ac_booking']:
                messages.append({
                    'sentBy': 'Bot',
                    'content': responses[result],
                    'url': AC_BOOK_URL[accomodation_tag]
                })

            case ['ac_image']:
                messages.append({
                    'sentBy': 'Bot',
                    'content': responses[result],
                    'url': AC_HOTEL_IMAGES[accomodation_tag]
                })

            case ['ac_room']:
                messages.append({
                    'sentBy': 'Bot',
                    'first_text': responses[result][accomodation_tag]['Description'][0],
                    'content': responses[result][accomodation_tag]['Description'][1:],
                    'room_image': responses[result][accomodation_tag]['Images']
                })

            case [('ac_landmark' | 'ac_fnb_offsite')]:
                bot_responses = responses[result][accomodation_tag]
                pick_one = random.choice(bot_responses)
                messages.append({
                    'sentBy': 'Bot',
                    'content': pick_one
                })
            
            case ['ac_clear']:
                other_options = [hotel for hotel in HOTELS if hotel != accomodation_tag]
                accomodation_tag = random.choice(other_options)

                with open('/Users/USER/Downloads/IAI/app/views/database/tag.txt', 'w') as get_tag:
                    get_tag.write(accomodation_tag)
                
                messages.append({
                    'sentBy': 'Bot',
                    'content': responses[result][accomodation_tag],
                    'url': AC_URL[accomodation_tag]
                })


        return render_template(
                'chatbot.html', 
                messages=messages
            )
    
    if result == 'ac_restaurant' and accomodation_tag:
        options = ["Onsite", "Offsite"]
        messages.append({
            'sentBy': 'Bot',
            'content': responses[result]
        })

        return render_template(
                'chatbot.html', 
                messages=messages,
                options=options
            )
    
    if result in AC_RELATED:
        messages.append({
            'sentBy': 'Bot',
            'content': responses[result][accomodation_tag]
        })

        return render_template(
                'chatbot.html', 
                messages=messages
            )

    if result in GENERAL:
        intentions = responses[result]
        random_response = random.choice(intentions)

        messages.append({
            'sentBy': 'Bot',
            'content': random_response
        })

        return render_template('chatbot.html', messages=messages)
    
    # Callback Intent 
    messages.append({
            'sentBy': 'Bot',
            'content': 'Sorry, I could not understand you.'
        })

    return render_template('chatbot.html', messages=messages)
