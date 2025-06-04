from flask import Flask
from models import db
from routes import main as main_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)