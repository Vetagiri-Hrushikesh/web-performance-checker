from flask import Flask
from flask_cors import CORS
from .lighthouse import lighthouse_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object('app.lighthouse.config.Configuration')
    app.register_blueprint(lighthouse_bp, url_prefix='/api/lighthouse')
    return app
