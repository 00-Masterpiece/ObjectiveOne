from flask_login import LoginManager
from flask import Flask
from models import db, User
import os
from sqlalchemy import text

from dotenv import load_dotenv
load_dotenv()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from routes import main as main_blueprint
app.register_blueprint(main_blueprint)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)