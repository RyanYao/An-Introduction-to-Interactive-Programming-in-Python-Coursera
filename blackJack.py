# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = 0
playerHand = 0
casinoHand = 0
score = [0, 0]
message = ""
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self, playerOrDealer):
        self.cardList = []
        self.isPlayer = playerOrDealer

    def __str__(self):
        ret = "Hand contains"
        for card in self.cardList:
            print type(card)
            print card
            ret += " "
            ret += card.suit
            ret += card.rank
        return ret

    def add_card(self, card):
        self.cardList.append(card)

    def get_value(self):
        value = 0
        hasAce = False
        for i in self.cardList:
            if i.rank=="A":
                hasAce = True
            value += VALUES[i.rank]
        if hasAce and value+10<=21:
            return value+10
        else:
            return value
   
    def draw(self, canvas, pos):
        for card in self.cardList:
            if not self.isPlayer and self.cardList.index(card)==0:
                canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, 
                                  [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
            else:
                card.draw(canvas, [pos[0]+self.cardList.index(card)*100 , pos[1]])
        
    
# define deck class
class Deck:
    def __init__(self):
        self.cardList = [];
        for s in SUITS:
            for r in RANKS:
                card = Card(s,r)
                self.cardList.append(card)
        random.shuffle(self.cardList)

    def shuffle(self):
        random.shuffle(self.cardList)

    def deal_card(self):
        return self.cardList.pop()
    
    def __str__(self):
        ret = "Deck contains"
        for card in self.cardList:
            ret += " "
            ret += card.suit
            ret += card.rank
        return ret

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, playerHand, casinoHand, message
    if in_play:
        score[0] += 1
    deck = Deck()
    playerHand = Hand(True)
    casinoHand = Hand(False)
    playerHand.add_card( deck.deal_card() )
    casinoHand.add_card( deck.deal_card() )
    playerHand.add_card( deck.deal_card() )
    casinoHand.add_card( deck.deal_card() )
    in_play = True
    message = "hit or stand?"

def hit():
    global in_play, playerHand, deck, message
    if in_play:
        if playerHand.get_value()<21:
            playerHand.add_card(deck.deal_card())
            if playerHand.get_value()>21:
                message = "you busted"
                score[0] += 1
                casinoHand.isPlayer = True
                in_play = False
            else:
                message = "Hit again? or stand?"
        else:
            message = "you busted, player lost"
    else:
        message = "can't hit, new deal?"
       
def stand():
    global in_play, playerHand, casinoHand, deck, score, message
    casinoHand.isPlayer = True
    if in_play:
        if playerHand.get_value()<=21:
            while casinoHand.get_value()<17:
                casinoHand.add_card( deck.deal_card() )
              
            if casinoHand.get_value()>21:
                message = "you win, new game?"
                score[1] += 1
            else:
                if casinoHand.get_value()>=playerHand.get_value():
                    message = "you lost, new deal?"
                    score[0] += 1
                elif casinoHand.get_value()<playerHand.get_value():
                    message = "you win, new deal?"
                    score[1] += 1
        else:
            message = "you busted, new deal?"
            score[0] += 1
        in_play = False
    else:
        message = "game's over bro/sis, new deal?"

# draw handler    
def draw(canvas):
    global score, message
    playerHand.draw(canvas, [100, 400])
    casinoHand.draw(canvas, [100, 200])
    canvas.draw_text("Black Jack", [150, 50], 50, "white")
    canvas.draw_text("by Ryan Yao", [380, 50], 15, "white")
    if casinoHand.isPlayer:
        canvas.draw_text("Dealer:"+str(casinoHand.get_value()), [100, 180], 35, "white")
    else:
        canvas.draw_text("Dealer", [100, 180], 35, "white")
    canvas.draw_text("Player:"+str(playerHand.get_value()), [100, 380], 35, "white")
    canvas.draw_text("Scores", [600, 100], 30, "pink")
    canvas.draw_text("Dealer: "+str(score[0]), [600, 140], 25, "pink")
    canvas.draw_text("Player: "+str(score[1]), [600, 180], 25, "pink")
    canvas.draw_text(message, [300, 380], 35, "white")
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()