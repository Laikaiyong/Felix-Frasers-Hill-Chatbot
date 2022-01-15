from app.views import blueprint

from flask import render_template

# http://127.0.0.1:5000/chatbot
@blueprint.route('/chatbot', methods=['GET'])
def get_role():
    pass

@blueprint.route('/chatbot', methods=['POST'])
def add_role():
    pass