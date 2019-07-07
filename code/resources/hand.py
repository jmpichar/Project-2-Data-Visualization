from flask import redirect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.hand import HandModel
from models.blackjack import *

# api works with resources and the resource has to be a class
# define the Hand resource
class Hand(Resource):
    TABLE_NAME = 'hands'

    parser = reqparse.RequestParser()
    # parser.add_argument('winner',
    #     type=str,
    #     required=True,
    #     help="This field cannot be left blank"
    # )
    # parser.add_argument('p1_chips',
    #     type=float,
    #     required=False,
    #     help=""
    # )

    # Query the database and send the jsonified result

    #@jwt_required() # authenticate hand
    def get(self, id):

        hand = HandModel.find_by_id(id)
        if hand:
            return hand.json()
        return {'message': 'Hand not found'}, 404

    def post(self):
        data = Hand.parser.parse_args()
        game = GameModel()

        outcomes = game.run_simulation()
        for outcome in outcomes:
            # print(outcome)
            player_hand = outcome['player_hand']
            dealer_hand = outcome['dealer_hand']
            winner = outcome['winner']
            p1_chips = outcome['p1_chips']
            p2_chips = outcome['p2_chips']

            hand = HandModel(player_hand=player_hand, dealer_hand=dealer_hand, winner = winner,p1_chips=p1_chips,p2_chips=p2_chips)

            try:
                hand.save_to_db()
            except:
                raise
                return {'message':'an error occurred inserting the hand.'}, 500

        # return hand.json(), 201
        return redirect("/", code=302)

    def delete(self, id):
        hand = HandModel.find_by_id(id)

        if hand:
            item.delete_from_db()

        return {'message':'Hand deleted'}

    def put(self, id):
        data = Hand.parser.parse_args()

        hand = HandModel.find_by_id(id)

        # HandModel.insert(hand)
        if hand is None:
            hand = HandModel(id, data['winner'])
        else:
            hand.winner = data['winner']

        hand.save_to_db()

        return hand.json()

class HandList(Resource):
    def get(self):
        ''' query the database for all items. the query will perform
            the following SQL command:
                SELECT * FROM items
            Can be done using a list comprehesion or a lambda function:
            return {'items': list(map(lambda item: item.json() , ItemModel.query.all()))}
        '''
        return {'hands':[hand.json() for hand in HandModel.query.all()]}
