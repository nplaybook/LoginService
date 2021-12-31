from flask import Flask

def create_app() -> Flask:
    """Main caller to create Flask application"""

    from .route import view

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecret'
    app.register_blueprint(view, url_prefix="/")
    
    return app