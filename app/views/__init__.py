from flask import Blueprint, render_template

blueprint = Blueprint('views', __name__)

# Route Declaration
from app.views import chatbot, plans

@blueprint.route('/')
def index():
    return render_template('index.html')
    