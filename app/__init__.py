from flask import Flask, Blueprint

def create_app():
    app = Flask(__name__)

    from app.views import blueprint as views_bp
    app.register_blueprint(views_bp)

    return app