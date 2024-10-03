from flask import Blueprint

lighthouse_bp = Blueprint('lighthouse', __name__)

from .controllers.overview.circular_progress_controller import bp as circular_progress_bp

# Registering the circular_progress_bp controller under lighthouse Blueprint
lighthouse_bp.register_blueprint(circular_progress_bp, url_prefix='/overview')
