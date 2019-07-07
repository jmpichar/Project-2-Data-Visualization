from flask import Flask, render_template, request, redirect
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.player import Player, PlayerList
from resources.hand import Hand, HandList
from models.blackjack import GameModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# turn off flask sqlalchemy tracker
# will sqlalchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)



# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    return render_template("form.html")

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) # /auth

# api.add_resource(Scenario, '/scenario/<string:name>')
api.add_resource(Player, '/player/<string:name>')
api.add_resource(PlayerList, '/players')
api.add_resource(Hand, '/run_simulation')
api.add_resource(HandList, '/hands')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
