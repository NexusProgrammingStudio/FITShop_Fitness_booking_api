from flask import Flask

from db import db, init_db
from routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
