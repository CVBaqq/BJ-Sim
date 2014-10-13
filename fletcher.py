#!/bin/python3.3
import sys, Queue
from random import randint

numOfCards = 4*4  # 4 Deck times 4 of the same card in a deck
minimumBet = 10

def main(argv):
	playerMoney = 100
	iterations = argv[1]
	# Make a Deck composed of 4 decks
	cardMap = dict()
	deck = buildNewDeck()
	count = 0
	for i in range(0, int(iterations)):
		print "=========================NEW ROUND ( "+ str(count) + " )=========================="
		moneyBet = dict()
		moneyBet['1'] = minimumBet
		if len(deck) < 25:
			deck = buildNewDeck()
		playerHands = dict()
		playerHands['1'] = []
		playerHands['1'].append(deck.pop())
		dealerCards = []
		dealerCards.append(deck.pop())
		playerHands['1'].append(deck.pop())
		dealerCards.append(deck.pop()) # This card is revealed
		dealerSoftHand = isSoftHand(dealerCards)
		dealerSum = findBestSum(dealerCards)
		playerSum = findBestSum(playerHands['1'])
		print "Player money initially: " + str(playerMoney)
		print "Dealer's Hands: " + dealerCards[0] + ", " + dealerCards[1] 
		print "Player's Hands: " + playerHands['1'][0] + ", " + playerHands['1'][1]
		if dealerSum == 21:
			if playerSum == 21:
				# This is a push
				count += 1
				continue
			# Dealer has blackjack, player don't.
			playerMoney -= moneyBet['1']
			print "Dealer Wins"
			count += 1
			continue
		# Player has blackjack, dealer don't.
		if playerSum == 21:
			playerMoney += moneyBet['1'] * 3/2
			print "Player Wins"
			count += 1
			continue
		playerSoftHand = isSoftHand(playerHands['1'])

		#print "Deck cards left: " + str(len(deck))
		callQuits = False
		handCount = 1
		while not callQuits:
			if len(playerHands[str(handCount)]) == 1:
				playerHands[str(handCount)].append(deck.pop())
			shouldPlayerSplit = False
			shouldPlayerDoubleDown = False
			shouldPlayerHit = False
			print "Current Playing Hand: " + str(handCount)
			print "Current Cards: " + str(playerHands[str(handCount)]) 
			shouldPlayerSplit = shouldPlayerSplitHand(dealerCards, playerHands[str(handCount)])
			shouldPlayerDoubleDown = shouldPlayerDoubleDownHand(dealerCards, playerHands[str(handCount)])
			shouldPlayerHit = shouldPlayerHitHand(dealerCards, playerHands[str(handCount)])

			print "Should Player Split: " + str(shouldPlayerSplit)
			print "Should Player Double Down: " + str(shouldPlayerDoubleDown)
			print "Should Player Hit: " + str(shouldPlayerHit)
			if shouldPlayerSplit:
				nextHand = len(playerHands) + 1
				print "We're splitting to hand " + str(nextHand)
				moneyBet[str(nextHand)] = 0
				moneyBet[str(nextHand)] = moneyBet[str(handCount)]

				playerHands[str(nextHand)] = []
				playerHands[str(nextHand)].append(playerHands[str(handCount)].pop())
				playerHands[str(handCount)].append(deck.pop())
				continue
			
			if shouldPlayerDoubleDown:
				currentBet = moneyBet[str(handCount)]
				moneyBet[str(handCount)] = currentBet * 2
				print "Doubled down money: " + str(moneyBet[str(handCount)])
				playerHands[str(handCount)].append(deck.pop())
				handCount += 1
				if handCount > len(playerHands):
					break
				else:
					continue

			if shouldPlayerHit:
				playerHands[str(handCount)].append(deck.pop())
				continue
			else:
				handCount += 1

			if handCount > len(playerHands) and not shouldPlayerSplit and not shouldPlayerDoubleDown and not shouldPlayerHit:
				callQuits = True 
		print "Player's final hands: " + str(playerHands)
		print "Bets on all hands: " + str(moneyBet)
		while dealerSum < 17:
			dealerCards.append(deck.pop())
			print "Dealer's Sum: " + str(dealerSum)
			print "Dealer's Hand: " + str(dealerCards)
			dealerSum = findBestSum(dealerCards)
		if dealerSum > 21:
			print "Dealer Bust."
			# Dealer Bust
			for handnumber in range(1, len(playerHands) + 1): 
				handSum = findBestSum(playerHands[str(handnumber)])
				if handSum <= 21:
					playerMoney += moneyBet[str(handnumber)]
					print "Player Hand " + str(handnumber) + " won " + str(moneyBet[str(handnumber)])
				else:
					playerMoney -= moneyBet[str(handnumber)]
					print "Player Hand " + str(handnumber) + " lost " + str(moneyBet[str(handnumber)])
		if dealerSum <= 21:
			print "Dealer less than or equal to 21"
			for handnumber in range(1, len(playerHands) + 1):
				handSum = findBestSum(playerHands[str(handnumber)])
				if handSum > 21:
					playerMoney -= moneyBet[str(handnumber)]
					print "Player Hand " + str(handnumber) + " lost" + str(moneyBet[str(handnumber)])
				elif handSum > dealerSum:
					playerMoney += moneyBet[str(handnumber)]
					print "Player Hand " + str(handnumber) + " won " + str(moneyBet[str(handnumber)])
				elif handSum < dealerSum:
					playerMoney -= moneyBet[str(handnumber)]
					print "Player Hand " + str(handnumber) + " lost " + str(moneyBet[str(handnumber)])
		print "Player money afterwards: " + str(playerMoney)
		count += 1
		print "=========================END ROUND=========================="


def findBestSum(hand):
	Sum = 0
	aceCount = 0
	print "Adding up cards: " + str(hand)
	for card in hand:
		if int(card) != 1:
			Sum += determineCardValue(card)
		else:
			aceCount += 1
	addingValue = True
	tryingTotal = aceCount * 11
	while addingValue:
		if Sum + tryingTotal <= 21:
			Sum += tryingTotal
			addingValue = False
		elif aceCount == 0 and Sum > 21:
			addingValue = False
		else:
			tryingTotal = tryingTotal - 11 + 1
		if aceCount == tryingTotal:
			Sum += tryingTotal
			addingValue = False
	print "Best Sum: " + str(Sum)
	return Sum
	

def shouldPlayerHitHand(dealerCards, playerHand):
	dealerFaceupCard = determineCardValue(dealerCards[1]) # Dealer's faceup card
	playerSum = findBestSum(playerHand)
	isHandSoft = False
	isHandSoft = isSoftHand(playerHand)
	if isHandSoft:
		if playerSum == 17:
			return True
		if playerSum == 18:
			if dealerFaceupCard >= 9 and dealerFaceupCard <= 13:
				return True
			if dealerFaceupCard == 1:
				return True
		if len(playerHand) == 2:
			if playerSum == 13 or playerSum == 14:
				if dealerFaceupCard != 5 and dealerFaceupCard != 6:
					return True
		
	if dealerFaceupCard >= 7 or dealerFaceupCard == 11:
		if playerSum < 17:
			return True
	if dealerFaceupCard >= 4 and dealerFaceupCard <= 6:
		if playerSum < 12:
			return True
	if dealerFaceupCard == 2 or dealerFaceupCard == 3:
		if playerSum < 13:
			return True
	return False


def shouldPlayerDoubleDownHand(dealerCards, playerHand):
	if len(playerHand) != 2:
		return False
	dealerFaceupCard = determineCardValue(dealerCards[1]) # Dealer's faceup card
	playerSum = findBestSum(playerHand)
	isHandSoft = False
	isHandSoft = isSoftHand(playerHand)
	if isHandSoft:
		if playerSum == 17 and dealerFaceupCard >= 3 and dealerFaceupCard <= 6:
			return True
	if dealerFaceupCard >= 4 or dealerFaceupCard <= 6:
		if playerSum == 10 or playerSum == 11:
			return True
	return False

def shouldPlayerSplitHand(dealerCards, playerHand):
	# Make sure the hand has only 2 cards
	if len(playerHand) != 2:
		return False
	playerFirstCard = determineCardValue(playerHand[0])
	playerSecondCard = determineCardValue(playerHand[1])
	dealerFaceupCard = determineCardValue(dealerCards[1]) # Dealer's Faceup card
	if playerFirstCard != playerSecondCard:
		return False
	# If it gets here, the hand is a pair.
	if dealerFaceupCard >= 2 and dealerFaceupCard <= 7:
		if playerFirstCard == 2 or playerFirstCard == 3 or playerFirstCard == 7:
			return True
	if dealerFaceupCard == 5 or dealerFaceupCard == 6:
		if playerFirstCard == 4:
			return True
	if dealerFaceupCard >= 3 and dealerFaceupCard <= 6:
		if playerFirstCard == 6:
			return True
	if dealerFaceupCard >= 2 and dealerFaceupCard <= 9 and dealerFaceupCard != 7:
		if playerFirstCard == 9:
			return True
	if playerFirstCard == 8 or playerFirstCard == 11:
		return True
	return False

def buildNewDeck():
	cardMap = dict()
	deck = []
	for card in range(1, 14):
		cardMap[str(card)] = numOfCards

	while len(deck) < 4*52:
		cardPicked = randint(1, 13)
		if cardMap[str(cardPicked)] != 0:
			cardMap[str(cardPicked)] -= 1
			deck.append(str(cardPicked))
	return deck

# Should return a value that doesn't bust
# Need a method that generates all combinations of sum that wouldn't bust
def determineCardValue(strValue):
	value = int(strValue)
	if value == 1:
		return 11
	elif value >= 10 and value <= 13:
		return 10
	else:
		return value

def isSoftHand(hand):
	Sum = 0
	aceCount = 0
	for card in hand:
		if int(card) != 1:
			Sum += determineCardValue(card)
		else:
			aceCount += 1
	addingValue = True
	tryingTotal = aceCount * 11
	while addingValue:
		if Sum + tryingTotal <= 21:
			Sum += tryingTotal
			addingValue = False
		elif aceCount == 0 and Sum > 21:
			addingValue = False
		else:
			tryingTotal = tryingTotal - 11 + 1
		if aceCount == tryingTotal:
			Sum += tryingTotal
			addingValue = False
	if tryingTotal == aceCount:
		return False
	return True

if __name__ == "__main__":
	main(sys.argv)
