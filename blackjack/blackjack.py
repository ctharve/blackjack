from random import shuffle, random

ranks = {'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'k'}
suits = {'S', 'H', 'C', 'D'}
cardvalues = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'k':10}
winningvalue = 21.0

class Card:
    def __init__(self, rank, suit):
        if (suit in suits and rank in ranks):
            self.rank = rank
            self.suit = suit            
        else:
            print("ERROR: Rank - {} or Suit - {} is invalid".format(suit, rank))

    def get_rank(self):
        return self.rank
    
    def get_value(self):
        return cardvalues.get(self.rank)
    
class Hand:
    def __init__(self):
        self.cards = []
        self.hasace = False
    
    def add_card(self, newcard):
        self.cards.append(newcard)         
    
    def get_value(self):
        value = 0
        for card in self.cards:
            if (card.get_rank() == 'A'):
                self.hasace = True
            value += card.get_value()              
        if (self.hasace and value<=11):
            value += 10
        return value
    
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        shuffle(self.cards)
        self.cards = iter(self.cards)
        self.nextcard = next(self.cards)
        self.__hascards = True
    
    def __increment_nextcard(self):
        self.nextcard = next(self.cards, None)
        if (not self.nextcard):
            self.__hascards = False
        
    def has_cards(self):
        return self.__hascards
    
    def deal_card(self):
        newcard = self.nextcard
        if (self.__hascards):            
            self.__increment_nextcard()
        else:
            print("ERROR: Deck is out of cards, start a new game.")
        return newcard

class Player:
    def __init__(self):
        self.hand = Hand()
        self.acceptancerate = 0.0
        self.busted = False
        
    def __update_acceptancerate(self):
        """
        Acceptance rate for randomly choosing to hit
        """
        self.acceptancerate = 1 - self.hand.get_value()/winningvalue
    
    def __update_buststatus(self):
        if (self.hand.get_value() > winningvalue):
            self.busted = True

    def take_card(self, newcard):
        self.hand.add_card(newcard)
        self.__update_acceptancerate()
        self.__update_buststatus()
        
    def should_hit(self):
        """
        Strategy is to randomly choose to hit with a decreasing acceptance 
        rate as the hand's value approaches 21
        """
        if (not self.busted and random() < self.acceptancerate):
            return True
        else:
            return False
        
    def get_value(self):
        return self.hand.get_value()
    
    def is_busted(self):
        return self.busted
    
class Game:
    """
    Game for two players
    """
    def __init__(self):
        self.deck = Deck()
        self.playerA = Player()
        self.playerB = Player()
        self.__results = {'playerA':0, 'playerB':0, 'currentWinner':None}
            
    def __deal(self):
        self.playerA.take_card(self.deck.deal_card())
        self.playerA.take_card(self.deck.deal_card())
        self.playerB.take_card(self.deck.deal_card())
        self.playerB.take_card(self.deck.deal_card())

        
    def __check_deck_and_hit_playerA(self):
        if (self.deck.has_cards()):
            self.playerA.take_card(self.deck.deal_card())            
        else:
            print("ERROR: Deck is out of cards, start a new game.")
            exit()
    
    def __check_deck_and_hit_playerB(self):
        if (self.deck.has_cards()):
            self.playerB.take_card(self.deck.deal_card())
        else:
            print("ERROR: Deck is out of cards, start a new game.")
            exit()
            
    def __hit_players(self, hita, hitb):
        if (not hita and not hitb):
            return
        if (hita):
            self.__check_deck_and_hit_playerA()
        if (hitb):
            self.__check_deck_and_hit_playerB()
        if (hita  and not self.playerA.is_busted() and hitb and not self.playerB.is_busted()):
            return self.__hit_players(self.playerA.should_hit(), self.playerB.should_hit())
        elif (hita and not self.playerA.is_busted() and not hitb):
            return self.__hit_players(self.playerA.should_hit(), False)
        elif (not hita and hitb and not self.playerB.is_busted()):
            return self.__hit_players(False, self.playerB.should_hit())
    
    def __update_results(self):
        scorea = self.playerA.get_value()
        scoreb = self.playerB.get_value()
        if (scorea==scoreb and not self.playerA.is_busted()):
            winner = 'tie'
        elif (scorea>scoreb):
            if(not self.playerA.is_busted()):
                winner = 'playerA'
            elif(not self.playerB.is_busted()):
                winner = 'playerB'
            else:
                winner = 'Double Bust!'
        elif (scoreb>scorea):
            if(not self.playerB.is_busted()):
                winner = 'playerB'
            elif(not self.playerA.is_busted()):
                winner = 'playerA'
            else:
                winner = 'Double Bust!'
        self.__results['playerA'] = scorea
        self.__results['playerB'] = scoreb
        self.__results['currentWinner'] = winner

    def print_results(self):
        print('PlayerA scored {} while PlayerB scored {}'.format(self.__results['playerA'], 
                                                                 self.__results['playerB']))
        print('{} is the winner'.format(self.__results['currentWinner']))

    def play(self):
        print("Starting the game, let's deal")
        self.__deal()
        self.__hit_players(self.playerA.should_hit(), self.playerB.should_hit())
        self.__update_results()
            
if __name__ == "__main__":
    print("Let's play a game of blackjack")
    newgame = Game()
    newgame.play()
    newgame.print_results()