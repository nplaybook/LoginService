from flask_sqlalchemy import SQLAlchemy
from flaskr.app import create_app

db = SQLAlchemy()
app = create_app(db)

if __name__ == '__main__':
    app.run()