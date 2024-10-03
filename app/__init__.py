from flask import Flask
from .lighthouse import lighthouse_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.lighthouse.config.Configuration')
    app.register_blueprint(lighthouse_bp, url_prefix='/api/lighthouse')
    return app
