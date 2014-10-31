#!/usr/bin/python
from __future__ import division
import sys, getopt, random

class Card(object):


    """Represents a standard playing card.
    Attributes:
        suit: integer 0-3
        rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "Jack", "Queen", "King"]
    values_lookup = {rank_names[1]: 1,
                     rank_names[2]: 2,
                     rank_names[3]: 3,
                     rank_names[4]: 4,
                     rank_names[5]: 5,
                     rank_names[6]: 6,
                     rank_names[7]: 7,
                     rank_names[8]: 8,
                     rank_names[9]: 9,
                     rank_names[10]: 10,
                     rank_names[11]: 10,
                     rank_names[12]: 10,
                     rank_names[13]: 10}
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human readable string representation."""
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __cmp__(self, other):
        """Compares this card to other, first by suit, then rank.
            Returns a positive number if this > other; negative if other > this;
            and 0 if they are equivalent.
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)

    def get_rank_for_split(self):
        return get_label(self.rank)

    def get_dealer_label(self):
        label = get_label(self.rank)
        if label == 'T':
            return '10'
        elif label == 'A':
            return '1'
        return label

    def get_value(self):
        return Card.values_lookup[Card.rank_names[self.rank]]

    def isAce(self):
        if self.rank == Card.suit_names[1]:
            return True
        else:
            return False

def get_label(card_rank):
    str_rank = Card.rank_names[card_rank]
    if str_rank == '10':
        return 'T'
    elif str_rank == 'Jack':
        return 'T'
    elif str_rank == 'Queen':
        return 'T'
    elif str_rank == 'King':
        return 'T'
    elif str_rank == 'Ace':
        return 'A'
    return str_rank

class Deck(object):
    """Represents a deck of cards.

    Attributes:
        cards: list of Card objects.
    """

    def __init__(self):
        self.cards = []

        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck."""
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num, game):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())
            lastcardrank = hand.cards[-1].rank
            if lastcardrank >= 2 and lastcardrank <= 6:
                game.count += 1
            elif lastcardrank >= 10 and lastcardrank <= 13:
                game.count -= 1
            elif lastcardrank == 1:
                game.count -= 1

    def moveCardsToDeck(self, otherDeck, num):
        """Moves the given number of cards to deck
        """
        for i in range(num):
            otherDeck.add_card(self.pop_card())

    def isEmpty(self):
        if not self.cards:
            return True
        else:
            return False

    def size(self):
        return len(self.cards)

    def destroy(self):
        del self.cards[:]

class Hand(Deck):


    """Represents a hand of playing cards.
        Attributes:
            cards
            label
            split
            splitted
            done: Boolean value indicating whether the hand is done being played
            isSoft: Is hand soft
            doubled: was the hand doubled down?
    """

    def __init__(self, label=''):
        self.cards = []
        self.label = label
        self.done = False
        self.isSoft = False
        self.doubled = False
        self.justSplited = False
        self.isAceSplit = False
        self.discarded = False

    def isSoftTotal(self):
        sum = 0
        acecount = 0
        for card in self.cards:
            if card.get_value() != 1:
                sum += card.get_value()
            else:
                acecount += 1
        aceused = acecount
        addingValue = True
        tryingTotal = acecount * 11
        while addingValue:
            if sum + tryingTotal <= 21:
                sum += tryingTotal
                addingValue = False
            elif acecount == 0 and sum > 21:
                addingValue = False
            else:
                tryingTotal = tryingTotal - 11 + 1
                aceused -= 1
            if acecount == tryingTotal:
                sum += tryingTotal
                addingValue = False
        if aceused > 0:
            return True
        return False


    def isHard(self):
        total = 0
        return False

    def totalSoftValue(self):
        if (self.isSoft()):
            print ''
        else:
            print 'Hand is hard'

    def burnCards(self):
        self.doubled = False
        self.isSoft = False
        self.justSplited = False
        del self.cards[:]
        self.isAceSplit = False
        self.discarded = False

    def printUpCards(self):
        if self.label == "Dealer":
            print self
        if self.label == "Player":
            print self

    def getLabelForSplit(self):
        if len(self.cards) == 2:
            if self.cards[0].rank == self.cards[1].rank: # Both cards have to be the same rank
                str = ''
                for card in self.cards:
                    if card.get_rank_for_split() == '':
                        return ''
                    str += card.get_rank_for_split()
                if str[0] != str[1]:
                    return ''
                return str
            else:
                return ''

        return ''

    def getTotalValue(self):
        sum = 0
        acecount = 0
        for card in self.cards:
            if card.get_value() != 1:
                sum += card.get_value()
            else:
                acecount += 1
        addingValue = True
        tryingTotal = acecount * 11
        while addingValue:
            if sum + tryingTotal <= 21:
                sum += tryingTotal
                addingValue = False
            elif acecount == 0 and sum > 21:
                addingValue = False
            else:
                tryingTotal = tryingTotal - 11 + 1
            if acecount == tryingTotal:
                sum += tryingTotal
                addingValue = False
        return sum


    def __str__(self):
        discarded = "Discarded: %r " % self.discarded
        cardstr = ', '.join(x.__str__() for x in self.cards)
        str = "Cards: %s " % (cardstr)
        return discarded + str

class Money(object):


    def __init__(self, initialamount):
        self.amount = initialamount
        self.highestamount = self.amount
        self.lowestamount = self.amount

    def initialBet(self, bet):
        self.amount -= bet.get_amount()

    def add(self, bets):
        for bet in bets:
            self.amount += bet.get_amount()

    def add(self, bet):
        self.amount += bet.get_amount()

    def add(self, amount):
        self.amount += amount

    def remove(self, amount):
        self.amount -= amount

    def double_down(self, bet):
        self.amount -= bet.get_amount() / 2

    def split(self, bet):
        self.amount -= bet.get_amount()

    def determinehighestamount(self):
        if self.amount > self.highestamount:
            self.highestamount = self.amount

    def determinelowestamount(self):
        if self.amount < self.lowestamount:
            self.lowestamount = self.amount

class Bet(object):

    """
        Represents a person's bet, only player
        amount: Total amount of money in bet
    """
    def __init__(self, initialamount=0):
        self.amount = initialamount

    def add(self, amount):
        self.amount += amount

    def initialBet(self, bet):
        self.amount -= bet.get_amount()

    def double_down(self):
        self.amount *= 2

    def destroy(self):
        self.amount = 0

    def get_amount(self):
        return self.amount

    def __str__(self):
        return str(self.amount)

class Person(object):
    """Represents a person playing the game, a player or dealer
    Attributes:
        label: name of the object (could be player or dealer)
        hands: list of hands in play
        bets: list of bets associated which each hand
        currentPlayingHand: The current hand we should take action on
        splitted: boolean indicating whether the person splitted, dealers can't split
    """
    def __init__(self, label='', money=0):
        self.hands = []
        self.bets = []
        # All person have an initial hand
        self.hands.append(Hand())
        self.label = label
        self.currentPlayingHand = 0
        self.splitted = False
        self.money = Money(money)
        self.win = 0
        self.lose = 0
        self.tie = 0
        self.numOfHands = 0

    def split(self):
        splitted = False
        #Dealer doesn't split
        if self.label == "Dealer":
            print "Can't split dealer cards"
            return splitted

        if len(self.hands[self.currentPlayingHand].cards) > 2:
            print "Can't split current playing hand. Contains 3 or more cards."
            return splitted

        newHand = Hand()
        newHand.justSplited = True
        newHand.add_card(self.hands[self.currentPlayingHand].cards.pop(-1))
        # Can't double when the splitted hands were aces
        if Card.rank_names[newHand.cards[0].rank] == "Ace":
            newHand.doubled = True
            newHand.justSplited = True
            newHand.isAceSplit = True
            self.hands[self.currentPlayingHand].isAceSplit = True
        self.hands[self.currentPlayingHand].justSplited = True

        splitted = True
        self.hands.append(newHand)
        self.splitted = True
        return splitted

    def add_card(self, deck, num, game):
        deck.move_cards(self.hands[self.currentPlayingHand], num, game)
        self.hands[self.currentPlayingHand].discarded = False

    #Dont deallocate first hand
    def discardallhands(self):
        for hand in self.hands:
            hand.burnCards()
        del self.hands[1:]
        self.currentPlayingHand = 0
        self.splitted = False
        for bet in self.bets:
            bet.destroy()
        del self.bets[:]

    # We will let the player play
    #TODO: Add adjustedsoft, adjustedhard, and adjustedsplit to param
    def play(self, dealercard, deck, basicStrat, adjustedStrat, game):
        finishedallhands = False
        if "Player" in self.label:
            while not finishedallhands:
                #First we bet
                #The priority of action is as follows
                # 1. Determine if we want to split, if we do, split it then add more cards to each split hands
                # 2. Determine if we want to double, no doubling after AA split.
                # 3. Determine if we want to hit or stand.
                # ============================================ ===================================================

                # Before we start playing, if the indicator indicates that we just split our hand,
                # add a card to the hand so we can play on.
                # Check whether we doubled on this hand. One corner case is when we split aces,
                # we only get one card.
                if self.hands[self.currentPlayingHand].discarded == False:
                    if self.hands[self.currentPlayingHand].justSplited:
                        deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                        self.hands[self.currentPlayingHand].justSplited = False
                        if self.hands[self.currentPlayingHand].isAceSplit:
                            if self.currentPlayingHand < len(self.hands) - 1:
                                self.currentPlayingHand += 1
                            else:
                                finishedallhands = True
                            continue

                    if self.hands[self.currentPlayingHand].doubled:
                        if self.currentPlayingHand < len(self.hands) - 1:
                            self.currentPlayingHand += 1
                        else:
                            finishedallhands = True
                        continue

                    splitLabelLookup = self.hands[self.currentPlayingHand].getLabelForSplit()
                    #Assume default action is not to split
                    if splitLabelLookup != '':
                        try:
                            splitAction = basicStrat.SplitMatrix[splitLabelLookup][dealercard]
                        except KeyError, e:
                            splitAction = 'N'
                        except IndexError, e:
                            splitAction = 'N'

                        if splitAction == 'Y':
                            didsplit = self.split()
                            if didsplit:
                                self.bets.append(Bet(self.bets[self.currentPlayingHand].get_amount()))
                                self.money.split(self.bets[-1])
                                self.numOfHands += 1
                                # We want to redo the loop so it can reevaluate itself
                                continue
                        #print 'Split Action: ' + splitAction
                    # Assume default action is to hit
                    softLabelLookup = str(self.hands[self.currentPlayingHand].getTotalValue())
                    if self.hands[self.currentPlayingHand].isSoftTotal():
                        try:
                            softAction = basicStrat.SoftMatrix[softLabelLookup][dealercard]
                            # We don't have mapping for 12 and under (AA is splitted), so move along to hard hitting
                        except KeyError, e:
                            softAction = 'H'
                        except IndexError, e:
                            softAction = 'H'

                        if softAction == 'H':
                            deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                            continue
                        elif softAction == 'D':
                            if len(self.hands[self.currentPlayingHand].cards) >= 2 and self.hands[self.currentPlayingHand].doubled:
                                if self.currentPlayingHand < len(self.hands) - 1:
                                    self.currentPlayingHand += 1
                                else:
                                    finishedallhands = True
                                continue
                            if len(self.hands[self.currentPlayingHand].cards) == 2:
                                deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                                self.hands[self.currentPlayingHand].doubled = True
                                self.bets[self.currentPlayingHand].double_down()
                                self.money.double_down(self.bets[self.currentPlayingHand])
                                if self.currentPlayingHand < len(self.hands) - 1:
                                    self.currentPlayingHand += 1
                                else:
                                    finishedallhands = True
                                continue
                            # just hit/give a card if we can't double
                            if len(self.hands[self.currentPlayingHand].cards) > 2 and self.hands[self.currentPlayingHand].doubled == False:
                                deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                                continue
                        # We want to see what our action is for a hard hand here.
                        # so continue the rundown
                        #elif softAction == 'S':

                    # Assume default action is to stand
                    hardLabelLookup = str(softLabelLookup)
                    #print "Hard Label Lookup: " + hardLabelLookup
                    #print "Dealer faceup card: " + dealercard
                    try:
                        hardAction = basicStrat.HardMatrix[hardLabelLookup][dealercard]
                        # use default hit if index can't be looked up
                        # may cause problems here
                    except KeyError, e:
                        hardAction = 'S'
                    except IndexError, e:
                        hardAction = 'S'

                    #print 'Hard Action: ' + hardAction
                    #print softLabelLookup
                    if hardAction == 'H':
                        deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                        continue
                    elif hardAction == 'F':
                        deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                        continue
                    elif hardAction == 'D':
                        if len(self.hands[self.currentPlayingHand].cards) >= 2 and self.hands[self.currentPlayingHand].doubled:
                            if self.currentPlayingHand < len(self.hands) - 1:
                                self.currentPlayingHand += 1
                            else:
                                finishedallhands = True
                            continue
                        if len(self.hands[self.currentPlayingHand].cards) == 2:
                            deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                            self.hands[self.currentPlayingHand].doubled = True
                            self.bets[self.currentPlayingHand].double_down()
                            self.money.double_down(self.bets[self.currentPlayingHand])
                            if self.currentPlayingHand < len(self.hands) - 1:
                                self.currentPlayingHand += 1
                            else:
                                finishedallhands = True
                            continue
                        # give a card if we can't double due to 3 or more cards already in hand
                        if len(self.hands[self.currentPlayingHand].cards) > 2 and self.hands[self.currentPlayingHand].doubled == False:
                            deck.move_cards(self.hands[self.currentPlayingHand], 1, game)
                            continue
                    elif hardAction == 'S':
                        if self.currentPlayingHand < len(self.hands) - 1:
                            self.currentPlayingHand += 1
                        else:
                            finishedallhands = True
                        continue
                    finishedallhands = True
                else:
                    if self.currentPlayingHand < len(self.hands) - 1:
                        self.currentPlayingHand += 1
                    else:
                        finishedallhands = True

        #Dealer has a different playing style
        # Stand on soft 17
        elif self.label == "Dealer":
            while not finishedallhands:
                totalValue = self.hands[0].getTotalValue()

                if totalValue < 17:
                    deck.move_cards(self.hands[0], 1, game)
                else:
                    finishedallhands = True

    def getDealerFaceupCard(self):
        if self.label == "Dealer":
            return self.hands[0].cards[1].get_dealer_label()

    def __str__(self):
        #hands = ', '.join([x.__str__() for x in self.hands])
        str = 'Person: %s, Splitted: %r \n' % (self.label,
                             self.splitted)
        for i in range(len(self.hands)):
            str += 'Hand %d: ' % i
            str += self.hands[i].__str__() + '\n'

        for i in range(len(self.bets)):
            str += 'Bet %d: ' % i
            str += self.bets[i].__str__() + '\n'

        return str


class BlackJackDeck(Deck):
    """Represents a BlackJack deck that contains specified amount of decks
    Attribute:
        cards = combined decks to play black jack
    """
    def __init__(self):
        num_decks = 6
        super(BlackJackDeck, self).__init__()
        for i in range(num_decks - 1):
            new_deck = Deck()
            new_deck.moveCardsToDeck(self, 52)

        self.shuffle()

class BlackJackGame(object):
    """Represents a black jack game that contains everything a black jack
    game has.
    Attributes:
        deck = a deck
        players: An list of players.
        dealer: dealer object

        BasicStrategy
        AdjustedStrategy
    """
    def __init__(self, rounds, dollar, numOfPlayers):
        self.deck = BlackJackDeck()
        self.rounds = rounds

        self.players = []

        for i in range(numOfPlayers):
            self.players.append(Person("Player" + str(i), dollar))

        self.dealer = Person("Dealer")
        # Contains all strategy
        self.BasicStrategy = BasicStrategy()
        self.AdjustedStrategy = AdjustedStrategy()
        # Keep track of a count
        self.count = 0
        # Number of dealings
        self.dealing = 0

    def play(self):
        gamenumber = 1
        while gamenumber <= self.rounds:
            print "===== Round " + str(gamenumber) + " ====="
            #Create new BlackJack Deck if current deck is empty
            self.deck = BlackJackDeck()
            #Burn a card before we start the round
            while self.deck.size() > 78:
                self.initBet(self.players, len(self.deck.cards))
                self.initHands(self.players, self.dealer, self.deck, self)
                self.dealing += 1
                print "===============================%d===========================" % self.dealing
                for i in range(len(self.players)):
                    print "Player %d money %d" % (i, self.players[i].money.amount)
                #Check if dealer has black jack, it's over.
                if self.dealer.hands[0].getTotalValue() == 21:
                    for player in self.players:
                        if player.hands[0].getTotalValue() == 21:
                            # This is a push. Don't take player money
                            player.money.add(player.bets[0].get_amount())
                            player.tie += 1
                        else:
                            player.hands[0].discarded = True
                            player.lose += 1
                        print player
                    print self.dealer
                    self.endRound()
                    continue
                else:
                    for player in self.players:
                        if player.hands[0].getTotalValue() == 21:
                            player.money.add(player.bets[0].get_amount() * 2.5)
                            player.win += 1
                            player.hands[0].discarded = True
                            print player
                            print self.dealer
                    if self.isAnyPlayersStillPlaying() == False:
                        self.endRound()
                        continue
                #================================================================

                # Player goes first
                for player in self.players:
                    player.play(self.dealer.getDealerFaceupCard(),
                                     self.deck,
                                     self.BasicStrategy,
                                     self.AdjustedStrategy,
                                     self)
                    print player

                # Stop playing if all hands of player has busted
                hasallplayersnotbusted = False
                for player in self.players:
                    for hand in player.hands:
                        if hand.getTotalValue() <= 21:
                            hasallplayersnotbusted = True
                if hasallplayersnotbusted == False:
                    determineWinners(self.players, self.dealer)
                    print self.dealer
                    for i in range(len(self.players)):
                        print "Player %d money %d" % (i, self.players[i].money.amount)
                    self.endRound()
                    continue

                # Dealer goes last
                # Dealer reveal, or when dealer starts hitting
                self.dealer.play(self.dealer.getDealerFaceupCard(),
                                 self.deck,
                                 self.BasicStrategy,
                                 self.AdjustedStrategy,
                                 self)
                print self.dealer

                #=============== Determine which hand won ===========================
                determineWinners(self.players, self.dealer)
                for i in range(len(self.players)):
                    print "Player %d money %d" % (i, self.players[i].money.amount)
                #============Stop and delete everything==============================
                print "Cards remaining in deck %d" % len(self.deck.cards)
                self.endRound()
            #Increase the game round
            gamenumber += 1
            self.count = 0
            self.deck.destroy()

        for i in range(len(self.players)):
            print "=============================================================="
            print "Player " + str(i)
            print "Player lowest money %d" % self.players[i].money.lowestamount
            print "Player highest money %d" % self.players[i].money.highestamount
            print "Player wins %d" % self.players[i].win
            print "Player losses %d" % self.players[i].lose
            print "Total Games %d" % self.dealing
            print "Player win rate %3.3f percent" % ((self.players[i].win / self.players[i].numOfHands) * 100)
            print "Player tie rate %3.3f percent" % ((self.players[i].tie / self.players[i].numOfHands) * 100)
            print "Player loss rate %3.3f percent" % ((self.players[i].lose / self.players[i].numOfHands) * 100)
            print "Total percentage %3.3f percent" % (((self.players[i].win / self.players[i].numOfHands) * 100) +
                                                      ((self.players[i].tie / self.players[i].numOfHands) * 100) +
                                                      ((self.players[i].lose / self.players[i].numOfHands) * 100))
            print "Player final money %d" % self.players[i].money.amount
            print "================================================"

    def endRound(self):
        for player in self.players:
            player.money.determinehighestamount()
            player.money.determinelowestamount()
            player.discardallhands()
        self.dealer.discardallhands()

    def isAnyPlayersStillPlaying(self):
        stillPlaying = False
        for player in self.players:
            for hand in player.hands:
                if hand.getTotalValue() <= 21 and hand.discarded == False:
                    stillPlaying = True
        return stillPlaying

    def initBet(self, players, remainingcards):
        deckremaining = round(remainingcards/52)
        truecount = int(round(self.count/deckremaining))
        print "Running Count: %d" % self.count
        print "Cards Remaining %d" % remainingcards
        print "Decks Remaining %d" % deckremaining
        print "True Count %d" % truecount

        if truecount <= 0:
            for player in players:
                player.bets.append(Bet(10))
                player.money.initialBet(player.bets[-1])
        elif truecount > 0:
            for player in players:
                player.bets.append(Bet(10 + (5 * truecount)))
                player.money.initialBet(player.bets[-1])

    def initHands(self, players, dealer, deck, game):
        # Deal hands alternating to players and dealer
        for player in players:
            player.add_card(deck, 1, game)
        dealer.add_card(deck, 1, game)
        for player in players:
            player.add_card(deck, 1, game)
        dealer.add_card(deck, 1, game)
        for player in players:
            player.numOfHands += 1
        dealer.numOfHands += 1

def determineWinners(players, dealer):
    dealerTotal = dealer.hands[0].getTotalValue()
    for player in players:
        if dealerTotal <= 21:
            for i in range(len(player.hands)):
                if player.hands[i].discarded == False:
                    playertotal = player.hands[i].getTotalValue()
                    if playertotal <= 21:
                        if playertotal > dealerTotal and playertotal <= 21:
                            # player win, take money
                            winnings = player.bets[i].get_amount() * 2
                            player.money.add(winnings)
                            player.win += 1
                        elif playertotal == dealerTotal:
                            #Push, push is a win
                            player.money.add(player.bets[i].get_amount())
                            player.tie += 1
                        elif playertotal < dealerTotal:
                            #Don't do anything if we lose, we already took the money
                            player.lose += 1
                    else:
                        player.lose += 1
        elif dealerTotal > 21: # dealer bust anything still in play wins
            for i in range(len(player.hands)):
                if player.hands[i].discarded == False:
                    playerTotal = player.hands[i].getTotalValue()
                    if playerTotal <= 21:
                        winnings = player.bets[i].get_amount() * 2
                        player.money.add(winnings)
                        player.win += 1
                    else:
                        player.lose += 1


class BasicStrategy(object):
    """Represents the basic strategy used for playing

    Attribute:
        HardMatrix: Contains matrix to hit, stand, double down
        SoftMatrix: Contains matrix to hit, stand and double down
        SplitMatrix: Contains matrix to split or not
    """
    def __init__(self):
        hardFile = open('hard')
        softFile = open('soft')
        splitFile = open('split')
        self.HardMatrix = dict()
        self.SoftMatrix = dict()
        self.SplitMatrix = dict()

        populateMatrix(self.HardMatrix, hardFile)
        populateMatrix(self.SoftMatrix, softFile)
        populateMatrix(self.SplitMatrix, splitFile)

        hardFile.close()
        softFile.close()
        splitFile.close()

def populateMatrix(matrix, file):
    lines = [line.strip() for line in file]
    # Evaluate the first line. Skip the first element because it's a filler (always 0)
    dealercards = lines[0].replace(" ", "").split(",")


    for playercombostring in lines[1:]:
        str = playercombostring.replace(" ", "").split(",")
        toDealerCardMap = dict()
        matrix[str[0]] = toDealerCardMap
        for i in range(len(dealercards)):
            if i == 0:
                continue
            map = matrix[str[0]]
            map[dealercards[i]] = str[i]

class AdjustedStrategy(object):
    """Represents the adjusted strategy used for playing

    Attribute:
        AdjustedHardMatrix: Contains matrix to hit, stand, or double down on index
        AdjustedSoftMatrix: Contains matrix to hit, stand and double down on index
        AdjustedSplitMatrix: Contains matrix to split or not on index
    """
    def __init__(self):
        hardFile = open('adjustedhard')
        softFile = open('adjustedsoft')
        splitFile = open('adjustedsplit')
        hardActionFile = open('adjustedhardaction')

        self.AdjustedHardMatrix = dict()
        self.AdjustedSoftMatrix = dict()
        self.AdjustedSplitMatrix = dict()
        self.AdjustedHardActionMatrix = dict()

        populateMatrix(self.AdjustedHardMatrix, hardFile)
        populateMatrix(self.AdjustedSoftMatrix, softFile)
        populateMatrix(self.AdjustedSplitMatrix, splitFile)
        populateMatrix(self.AdjustedHardActionMatrix, hardActionFile)

        hardFile.close()
        softFile.close()
        splitFile.close()
        hardActionFile.close()

def main(argv):
    dollar = ''
    rounds = ''
    players = ''
    try:
        opts, args = getopt.getopt(argv, "hd:r:p:", ["dollar=", "rounds=", "players="])
    except getopt.GetoptError:
        print 'counting.py -d <starting dollars> -r <number of rounds> -p <number of players>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'counting.py -d <starting dollars> -r <number of rounds> -p <number of players>'
            sys.exit()
        elif opt in ("-d", "--dollar"):
            dollar = arg
        elif opt in ("-r", "--rounds"):
            rounds = arg
        elif opt in ("-p", "--players"):
            players = arg

    game = BlackJackGame(int(rounds), int(dollar), int(players))
    game.play()

if __name__ == "__main__":
    main(sys.argv[1:])
