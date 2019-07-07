from db import db

class PlayerModel(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    strategy = db.Column(db.String(80))
    buyIn = db.Column(db.Float)
    chips = db.Column(db.Float)
    unitBet = db.Column(db.Float)
    # hand_id = db.Column(db.Integer, db.ForeignKey('hands.id'))
    # hand = db.relationship('HandModel')

    def __init__(self, name, strategy, buyIn, chips, unitBet):
        self.name = name
        self.strategy = strategy
        self.buyIn = buyIn
        self.chips = chips
        self.unitBet = unitBet

    def json(self):
        return {'name': self.name, 'strategy': self.strategy, 'buyIn':self.buyIn, 'chips':self.chips, 'unitBet':self.unitBet}

    @classmethod
    def find_by_name(cls, name):

        ''' The line:
            return PlayerModel.query.filter_by(name=name).first()
        performs:
        SELECT * FROM items WHERE name=name LIMIT 1
        Because its a class nethod we can use cls
        '''
        return cls.query.filter_by(name=name).first()

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
