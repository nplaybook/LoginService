from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

def create_app(db: SQLAlchemy) -> Flask:
    """Main caller to create Flask application"""

    from .routes.views import view
    from .routes.route import api

    app = Flask(__name__, template_folder="./routes/templates", static_folder="./routes/static")
    app.config['SECRET_KEY'] = 'mysecret'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATNIOS"] = False
    CORS(app)
    
    db.init_app(app)

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api/")
    
    app.debug=True
    return app