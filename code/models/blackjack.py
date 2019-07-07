
import random
from models.player import PlayerModel

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


# define hand class
class Hand:
    def __init__(self, name):
        # initialize the hand
        self.cards = []
        self.name = name

    def __str__(self):
        # return a string representation of a hand
        s = ""
        for i in range(len(self.cards)):
            s = s + " " + str(self.cards[i])
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace,
        # then add 10 to hand value if it doesn't bust
        hvalue = 0
        ace_cnt = 0

        for i in range(len(self.cards)):
            card = str(self.cards[i])
            cvalue = VALUES[card[1]]
            if cvalue == 1:
                ace_cnt += 1
            hvalue += cvalue

        for j in range(ace_cnt):
            if hvalue + 10 <= 21:
                hvalue += 10

        return hvalue


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object with 2 decks
        self.cards = []
        for i in range(2):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(suit, rank))

        size = len(self.cards)
        self.cut_card = int(size - (.7 * size))
        self.size = size

    def print_deck(self):
        for i in range(len(self.cards)):
            print(str(i) + ":" + str(self.cards[i]))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)

    def deal_card(self):
        # deal card from the deck
        return self.cards.pop()

    def __str__(self):
        # return a string representing the deck
        s = "Deck contains "
        for c in self.cards:
           s = s + " " +  str(c)
        return s


class Player:
    def __init__(self, name, buyIn, unitBet, strategy = 'flat'):
        self.name = name
        self.buyIn = buyIn
        self.chips = self.buyIn
        self.unitBet = unitBet
        self.bet = unitBet
        self.strategy = strategy
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consec_losses = 0
        self.max_consec_wins = 0

    def buy_chips(self, amount):
        self.buyIn += amount
        self.chips += amunt

class GameModel(Deck):
    def __init__(self):
        outcome = ""

    def new_shoe(self):
        # create a new deck and shuffle
        self.deck  = Deck()
        self.deck.shuffle()

    def deal(self):

        player_hand = Hand("player")
        dealer_hand = Hand("dealer")
        player_card1 = self.deck.deal_card()
        dealer_upcard = self.deck.deal_card()

        player_card2 = self.deck.deal_card()
        dealer_downcard = self.deck.deal_card()

        # assign cards
        player_hand.add_card(player_card1)
        player_hand.add_card(player_card2)

        dealer_hand.add_card(dealer_downcard)
        dealer_hand.add_card(dealer_upcard)

        # print(f"Dealer's up card: {dealer_upcard}")
        self.dealer_upcard = dealer_upcard

        self.player_hand = player_hand
        self.dealer_hand = dealer_hand

    def stand(self):
        player_hand_value = self.player_hand.get_value()
        dealer_hand_value = self.dealer_hand.get_value()

        while dealer_hand_value < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
            dealer_hand_value = self.dealer_hand.get_value()

        # check outcome
        if dealer_hand_value > 21:
            print("Dealer busted")
            self.outcome = 'player'
        elif dealer_hand_value == player_hand_value:
            self.outcome = "push"
        elif dealer_hand_value > self.player_hand.get_value():
            self.outcome = "dealer"
        else:
            self.outcome = "player"

    def hit_or_stand(self):

        dealer_upcard_value = self.dealer_upcard.value
        player_hand_value = self.player_hand.get_value()

        if (dealer_upcard_value == 1) or (dealer_upcard_value > 6):
            while self.player_hand.get_value() < 17:
                # self.hit()
                self.player_hand.add_card(self.deck.deal_card())

            if self.player_hand.get_value() > 21:
                print("Player Busted")
                self.outcome = "dealer"
                player_cards = f'{self.player_hand}'.strip()
                dealer_cards = f'{self.dealer_hand}'.strip()
                return {
                    "player_hand":player_cards,
                    "dealer_hand":dealer_cards,
                    "winner":self.outcome
                }
            else:
                self.stand()
        else:
            self.stand()

        player_cards = f'{self.player_hand}'.strip()
        dealer_cards = f'{self.dealer_hand}'.strip()
        return {"player_hand":player_cards,"dealer_hand":dealer_cards, "winner":self.outcome}

    def update_bank(self, player, winner):
        global bank_roll

        if winner == 'player':
            player.chips += player.bet
            player.consecutive_losses = 0
            player.consecutive_wins += 1
            player.max_consec_wins = max(player.consecutive_wins, player.max_consec_wins)
            if (player.consecutive_wins >= 3) and (player.strategy == "progressive"):
                player.bet *= 1.5
        elif winner == 'dealer':
            player.chips -= player.bet
            player.consecutive_wins = 0
            player.consecutive_losses += 1
            player.max_consec_losses = max(player.consecutive_losses, player.max_consec_losses)
            player.bet = player.unitBet

        return player.chips

    def run_simulation(self):
        # get play info from the database
        playerInfo = [player.json() for player in PlayerModel.query.all()]

        # create player
        players = []
        for p in playerInfo:
            player_name = p['name']
            player_strategy = p['strategy']
            player_buyIn = p['buyIn']
            player_chips = p['chips']
            player_unitBet = p['unitBet']
            a_player = Player(player_name,player_buyIn, player_unitBet, strategy= player_strategy)
            players.append(a_player)


        # create a deck and shuffle cards
        self.new_shoe()

        # deal cards
        results = []
        for i in range(2000):
            cards_left = len(self.deck.cards)
            # print('Cards left in shoe: ', cards_left)
            if  cards_left < self.deck.cut_card:
                self.new_shoe()
            self.deal()
            result = self.hit_or_stand()

            # This code won't work if we have more than 2 players
            p = players[0]
            self.update_bank(p, result['winner'])
            result['p1_chips'] = p.chips

            p = players[1]
            self.update_bank(p, result['winner'])
            result['p2_chips'] = p.chips

            results.append(result)

            print(f'Player hand: {self.player_hand}: Value: {self.player_hand.get_value()}')
            print(f'Dealer hand: {self.dealer_hand}: Value: {self.dealer_hand.get_value()}')
            #print(f"Winner: {result['winner']} Total chips: {p1.chips} {p2.chips}\n")
            # print(results)
        print(f'{players[0].name} stats: chips: {players[0].chips}')
        print(f'{players[1].name} stats: chips: {players[1].chips}')
        print(f'Player max consecutive wins: {players[0].max_consec_wins}')
        print(f'Player max consecutive losses: {players[0].max_consec_losses}')

        # update player stats
        # to modify to work with multiple players
        for p in playerInfo:
            player = PlayerModel.find_by_name(p['name'])

            if players[0].name == p['name']:
                player.chips = players[0].chips
            elif players[1].name == p['name']:
                player.chips = players[1].chips

            player.save_to_db()

        return results
