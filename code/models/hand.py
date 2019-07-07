from db import db

class HandModel(db.Model):
    __tablename__ = "hands"

    id = db.Column(db.Integer, primary_key=True)
    player_hand = db.Column(db.String(80))
    dealer_hand = db.Column(db.String(80))
    winner = db.Column(db.String(80))
    p1_chips = db.Column(db.Float)
    p2_chips = db.Column(db.Float)


    def __init__(self, player_hand, dealer_hand, winner, p1_chips, p2_chips):
        self.dealer_hand = dealer_hand
        self.player_hand = player_hand
        self.winner = winner
        self.p1_chips = p1_chips
        self.p2_chips = p2_chips

    def json(self):
        return {
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'winner': self.winner,
            'p1_chips': self.p1_chips,
            'p2_chips': self.p2_chips
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # SELECT * FROM hands WHERE id=_id LIMIT 1

    def save_to_db(self):
        ''' Insert the current object to the database. Can do an
            update and insert. The session is a collection of obejects
            that can be written to the database'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        ''' delete an itemModel from the database. This will do:
            "DELETE FROM items WHERE name=?"
        '''
        db.session.delete(self)
        db.session.commit()
