from flask import render_template, request, redirect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.player import PlayerModel


# api works with resources and the resource has to be a class
# define the Player resource
class Player(Resource):
    TABLE_NAME = 'players'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('strategy',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('buyIn',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument('chips',
        type=float,
        required=False,
        help=""
    )

    parser.add_argument('unitBet',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    def get(self, name):
        player = PlayerModel.find_by_name(name)
        if player:
            return player.json()
        return {'message': 'Player not found'}, 404

    def post(self, name):
        data = Player.parser.parse_args()

        # not getting the name correctly from the url
        name = data["name"]

        if PlayerModel.find_by_name(name):
            return {'message': f'A player with name {name} already exists'}, 400

        data = Player.parser.parse_args()
        strategy = data['strategy']
        buyIn = data["buyIn"]
        chips = data["buyIn"]
        unitBet = data["unitBet"]

        player = PlayerModel(name=name, strategy=strategy, buyIn=buyIn, chips=chips, unitBet=unitBet)
        # print(f'{name}:{strategy}:{buyIn}:{chips}{unitBet}')

        try:
            player.save_to_db()
        except:
            #raise
            return {'message':'an error occurred inserting the player.'}, 500

        #return player.json(), 201

        return redirect("/", code=302)

    def delete(self, name):
        player = PlayerModel.find_by_name(name)

        if player:
            item.delete_from_db()

        return {'message':'Player deleted'}

    def put(self, name):
        data = Player.parser.parse_args()

        # not getting the name correctly from the url
        name = data["name"]

        player = PlayerModel.find_by_name(name)

        # PlayerModel.insert(player)
        if player:
            # update attributes
            player.strategy = data['strategy']
            player.buyIn = data["buyIn"]
            player.chips = data["buyIn"]
            player.unitBet = data["unitBet"]
        else:
            player = PlayerModel(name=name, strategy=strategy, buyIn=buyIn, chips=chips, unitBet=unitBet)

        player.save_to_db()

        return player.json()

class PlayerList(Resource):
    def get(self):
        ''' query the database for all items. the query will perform
            the following SQL command:
                SELECT * FROM items
            Can be done using a list comprehesion or a lambda function:
            return {'players': list(map(lambda x: x.json() , PlayerModel.query.all()))}
        '''
        return {'players':[player.json() for player in PlayerModel.query.all()]}
        #return {[player.json() for player in PlayerModel.query.all()]}
