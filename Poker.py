from sys import exit
from os import system
import random

clear = lambda: system('cls')
clear()

class deck():
	def __init__(self):
		self.cards = []
		self.pot = 0
		self.dealPosition = 0
		self.smallBlinds = 5
		self.bigBlinds = 10
		self.currentBet = 0
		self.fiveCards = []
		self.foldPlayerCount = 0

	def resetDeck(self):
		self.cards = ['♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K', '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K', '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K', '♠A', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K']
		random.shuffle(self.cards)
		self.fiveCards = ['**'] * 5
		self.currentBet = 0
		self.pot = 0
		self.foldPlayerCount = 0

	def drawCard(self):
		return self.cards.pop(0)

	def dealCards(self):
		i=0
		while(i<2):
			for each in players:
				each.cards.append(self.drawCard())
			i+=1

	def betCalcs(self,person,bet):
		if bet + person.currentBet > self.currentBet:
			self.currentBet = bet + person.currentBet
		person.currentBet = person.currentBet + bet
		person.totalBet = person.totalBet + bet
		person.money = person.money - bet
		self.pot = self.pot + bet

	def takeBlinds(self):
		clear()
		currentPlayer = players[self.dealPosition % playerCount]
		self.betCalcs(currentPlayer, self.smallBlinds)
		print(f"\n\n {currentPlayer.name} has placed ${self.smallBlinds} as Small Blinds")
		
		self.dealPosition+=1

		currentPlayer = players[self.dealPosition % playerCount]
		self.betCalcs(currentPlayer, self.bigBlinds)
		input(f"\n\n {currentPlayer.name} has placed ${self.bigBlinds} as Big Blinds")
		
	def takeBet(self):
		while True:
			try:
				return int(input("\n 	Please place your bet:  "))
			except:
				input("\n 		Please give me a number.... Dumbass!")

	def flop(self):
		self.fiveCards[0] = self.cards[1]
		self.fiveCards[1] = self.cards[2]
		self.fiveCards[2] = self.cards[3]

	def turn(self):
		self.fiveCards[3] = self.cards[5]
		
	def river(self):
		self.fiveCards[4] = self.cards[7]

	def pokerTable(self, person):
		clear()
		print("\n			...~~~|!|>---<__ BoomPa's CASINO __>---<|!|~~~... ")
		print(f"\n\n\n 	{person.name}'s Money: ${person.money}" + "					{:>5} Value: ${}".format("Pot", self.pot))
		print(f"\n\n 				[{self.fiveCards[0]}]  [{self.fiveCards[1]}]  [{self.fiveCards[2]}]  [{self.fiveCards[3]}]  [{self.fiveCards[4]}]")
		print("\n\n 			[1]. Show Cards")
		ask = False
		if self.currentBet - person.currentBet == 0 and not person.check:
			ask = True
			print(" 			[2]. Check")
			print(" 			[3]. Raise")
			print(" 			[4]. Fold")
			print(" 			[5]. ALL IN")
		elif self.currentBet - person.currentBet >= person.money:
			ask = True
			print(" 			[2]. ALL IN")
			print(" 			[3]. Fold")
		elif self.currentBet - person.currentBet < person.money:
			ask = True
			if self.currentBet - person.currentBet == 0:
				ask = False
			print(f" 			[2]. Call ${self.currentBet - person.currentBet}")
			print(" 			[3]. Raise")
			print(" 			[4]. Fold")
			print(" 			[5]. ALL IN")
		if ask:
			return input("\n\n 	Please enter your choice: ")
		else:
			return "2"

	def getChoice(self, person):
		while True:
				choice = dealer.pokerTable(person)
				if choice not in ['1', '2', '3', '4', '5','exit']:
					input("\n 					****_____Dumbass_____****")
				elif self.currentBet - person.currentBet >= person.money and (choice == '4' or choice == '5'):
					input("\n 					****_____Dumbass_____****")
				else:
					break
		return choice

	def doChoice(self, person, choice):
		while choice == '1':
			clear()
			input(f"\n\n\n\n\n 					[{person.cards[0]}]  [{person.cards[1]}]")
			choice = self.getChoice(person)
		if choice == '2':
			if self.currentBet - person.currentBet <= person.money:
				bet = self.currentBet - person.currentBet
			else:
				bet = person.money
		if choice == '3':
			if self.currentBet - person.currentBet >= person.money:
				choice = '4'
			else:
				person.check = True
				while True:
					bet = self.takeBet()
					if bet<=0:
						input("\n 					****_____Dumbass_____****")
					elif bet < self.currentBet:
						input("\n 					That's not enough")
					elif bet <= person.money:
						break
					else:
						input("\n 		Bitch! You ain't got that kinda money on table!")
		if choice == '4':
			bet = 0
			person.fold = True
			person.handScore = -1
			self.foldPlayerCount += 1
		if choice == '5':
			bet = person.money	
		if choice == 'exit':
			exit()

		self.betCalcs(person, bet)

	def pokerHands(self,score):
		handsDict = { -1 : "Fold" , 0 : "Won by Default", 1 : "High Card", 2 : "One Pair", 3 : "Two Pairs", 4 : "Three of a Kind", 5 : "Straight", 6 : "Flush", 7 : "Full House", 8 : "Four of a Kind", 9 : "Straight Flush", 10 : "Royal Flush"}
		return handsDict[score]

	def cardValue(self, card):
		valuesDict = {"A" : 14, "2" : 2, "3" : 3,  "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "J" : 11, "Q" : 12, "K" : 13}
		return valuesDict[card[1::]]

	def cardsSorter(self,cards):
		itercount = len(cards) - 1
		sort = False
		while not sort:
			l=0
			sort = True
			while l < itercount:
				if self.cardValue(cards[l]) > self.cardValue(cards[l+1]):
					temp = cards[l]
					cards[l] = cards[l+1]
					cards[l+1] = temp
					sort = False
				l+=1
		return cards

	def calcFinalHand(self, person):
		i, j, stCount, isFlush = person.handAttributes
		sevenSet = person.cards + self.fiveCards
		sevenSet = self.cardsSorter(sevenSet)
		tempHand = []
		# Checking for pairs
		l = 0
		count = "i"
		while l < 6:
			if sevenSet[l][1::] == sevenSet[l+1][1::]:
				if len(tempHand) == 0 or tempHand[len(tempHand)-1] != sevenSet[l]:
					tempHand.append(sevenSet[l])
				tempHand.append(sevenSet[l+1])
			l+=1
		if len(tempHand) < 5:
			l = 0
			reqCards = 5 - len(tempHand)
			while l < reqCards:
				if sevenSet[::-1][l] not in tempHand:
					tempHand.append(sevenSet[::-1][l])
				else:
					reqCards+=1
				l+=1
		if len(tempHand) > 5:
			# preparing a temporary values associated to cards. Based on this list, we can sort the cards list as with respective indexes of this list when it gets sorted.
			tempHandValList = []
			for each in tempHand:
				tempHandValList.append(self.cardValue(each))
			compCardVal = tempHandValList[0]
			count = 1
			l = 0
			while l < len(tempHandValList)-1:
				if tempHandValList[l] == tempHandValList[l+1]:
					count+=1
					# Adding 15 for 3 of a kind and 30 for 4 of a kind to increase strenght of cards. 
					# So that when these cards are sorted we get a 3 of a kind or 4 of a kind before higher one pairs or 2 pairs. 
					# Implicitly we always get a higher hand here.
					if count == 4:
						for each in tempHandValList:
							if each - 15 == compCardVal:
								each = each + 15 # Because already a 15 was added when 3 of a kind is detected
							elif each == compCardVal:
								each = each + 30
					elif count == 3:
						for each in tempHandValList:
							if each == compCardVal:
								each = each + 15
				else:
					compCardVal = tempHandValList[l+1]
					count = 1
				l+=1
			# Bubble sorting both tempHandValList and tempHand based on the indexes from tempHandValList
			sort = False
			l = 0
			while not sort:
				sort = True
				if tempHandValList[l] > tempHandValList[l+1]:
					temp = tempHandValList[l]
					tempHandValList[l] = tempHandValList[l+1]
					tempHandValList[l+1] = temp

					temp = tempHand[l]
					tempHand[l] = tempHand [l+1]
					tempHand[l+1] = temp
					sort = False
				l+=1
			# Trimming the length to 5 - The list was sorted in ascending order above
			tempHand = tempHand[len(tempHand)-5:][::-1]
		# Finding i and j
		temp = []
		l = 0
		count = 1
		while l < 4:
			if tempHand[l][1::] == tempHand[l+1][1::]:
				count+=1
			else:
				temp.append(count)
				count = 1
			l+=1
		temp.append(count)

		i,j = temp[0], temp[1]

		# Checking for general Flush
		flushSuit = ""
		hearts, diamonds, spades, clubs = [],[],[],[]
		for each in sevenSet:
			if each[0] == '♥':
				hearts.append(each)
			elif each[0] == '♦':
				diamonds.append(each)
			elif each[0] == '♠':
				spades.append(each)
			else:
				clubs.append(each)
		for each in [hearts, diamonds, spades, clubs]:
			if len(each)>=5:
				isFlush = "Normal"
				flushSuit = each[0][0]
				tempHand = self.cardsSorter(each)
				tempHand = tempHand[len(tempHand)-5:]
				break

		# Checking for straight
		prevCard = sevenSet[0]
		temp = []
		l = 0
		while l < 6:
			enterFlag = False
			v1 = self.cardValue(sevenSet[l])
			v2 = self.cardValue(sevenSet[l+1])
			if v1 + 1 == v2:
				enterFlag = True
				stCount+=1
				if len(temp) == 0 or temp[len(temp)-1] != sevenSet[l] :
					temp.append(sevenSet[l])	
				temp.append(sevenSet[l+1])
				prevCard = sevenSet[l+1]

			if v1 == v2 and not enterFlag:
				enterFlag = True
				if sevenSet[l][0] == flushSuit:
					if len(temp) == 0:
						temp.append(sevenSet[l])
					elif v1 == self.cardValue(temp[len(temp)-1]):
						temp[len(temp)-1] = sevenSet[l]

				elif sevenSet[l+1][0] == flushSuit:
					if len(temp) == 0:
						temp.append(sevenSet[l+1])
					elif v2 == self.cardValue(temp[len(temp)-1]):
						temp[len(temp)-1] = sevenSet[l+1]
				else:
					if len(temp) == 0:
						temp.append(sevenSet[l+1])
					else:
						temp[len(temp)-1] = sevenSet[l+1]
				
			if (v1+1 != v2) and not enterFlag:
				if stCount >=5:
					break
				else:
					stCount = 1
					temp = []
			l+=1
		if stCount>=5:
			temp = temp[len(temp)-5:]
			# Checking for straight flush or Royal Flush
			if temp[0][0] == temp[1][0] == temp[2][0] == temp[3][0] == temp[4][0]:
				isFlush = "RARE"
			if isFlush == 'Normal':
				temp = tempHand # Keeping the Flush instead of Straight
			tempHand = temp
		person.finalHand = tempHand
		return i,j,stCount,isFlush

	def calcHandScore(self, person):
		[i,j,stCount,isFlush] = person.handAttributes
		handScore = 0
		if i == 1 and j == 1:
			handScore = 1 # "High Card"
		if i == 2 or j == 2:
			handScore = 2 # "One Pair"
		if i == 2 and j == 2:
			handScore = 3 # "Two Pairs"
		if i == 3 or j == 3:
			handScore = 4 # "Three of a Kind"
		if stCount >=5:
			handScore = 5 # "Straight"
		if isFlush == "Normal":
			handScore = 6 # "Flush"
		if (i == 2 and j == 3) or (i == 3 and j == 2):
			handScore = 7 # "Full House"
		if i == 4 or j == 4:
			handScore = 8 # "Four of a Kind"
		if stCount >= 5 and isFlush == "RARE":
			handScore = 9 # "Straight Flush"
			if person.finalHand[4][1::] == "A":
				handScore = 10 # "Royal Flush"
		return handScore

	def calcHandStrength(self,person):
		sum = 0
		for each in person.finalHand:
			sum = sum + self.cardValue(each)
		return sum
	
	def sayWinner(self):
		clear()
		print("\n			...~~~|!|>---<__ BoomPa's CASINO __>---<|!|~~~... ")
		print("\n\n Cards on the table are...")
		print(f"\n 				{self.fiveCards}\n\n\n")
		if playerCount - dealer.foldPlayerCount != 1:
			for each in players:
				if not each.fold:
					each.handAttributes = self.calcFinalHand(each)
					each.handScore = self.calcHandScore(each)
			
			for each in players:
				each.finalScore = each.handScore
				each.remainingBet = each.totalBet

			for x in players:
				for y in players:
					if not x.fold and not y.fold and x!=y:
						if x.handScore > y.handScore:
							y.finalScore-=1
						elif x.handScore == y.handScore:
							s1 = self.calcHandStrength(x)
							s2 = self.calcHandStrength(y)
							if s1 > s2:
								y.finalScore-=1
							elif s1 < s2:
								x.finalScore-=1
							else:
								h1 = x.finalHand
								h2 = y.finalHand
								if x.handScore == "6":
									const = 4 # Compare in Right to left
								else:
									const = 0 # Compare left to right
								i = 0
								while i < 5:
									if self.cardValue(h1[i-const]) > self.cardValue(h2[i-const]):
										y.finalScore-=1
										break
									elif self.cardValue(h1[i-const]) < self.cardValue(h2[i-const]):
										x.finalScore-=1
										break
									i+=1

						else:
							x.finalScore-=1
			# preserving players list order
			playersDict = {}
			i = 0
			while i<playerCount:
				playersDict[i] = players[i]
				i+=1
			
			tpl = players # tpl = temporary list of players
			sort = False
			while not sort:
				sort = True
				i = 0
				while i<playerCount-1:
					if tpl[i].finalScore < tpl[i+1].finalScore:
						temp = tpl[i]
						tpl[i] = tpl[i+1]
						tpl[i+1] = temp
						sort = False
					i+=1

			p=0
			while p < playerCount-1:
				winAmt = 0
				curAmt = 0
				if tpl[p].finalScore > tpl[p+1].finalScore:
					i = 0
					remBet = tpl[p].remainingBet
					while i < playerCount:
						if remBet >= tpl[i].remainingBet:
							curAmt = tpl[i].remainingBet
							tpl[i].remainingBet = 0
						else:
							curAmt = remBet
							tpl[i].remainingBet -= remBet
						winAmt += curAmt
						i+=1
					if winAmt > 0:
						tpl[p].money += winAmt
						print("	{:<8} has won ${}  with {} = {}".format(tpl[p].name,winAmt,self.pokerHands(tpl[p].handScore),tpl[p].finalHand))
					p+=1

				elif tpl[p].finalScore == tpl[p+1].finalScore:
					i = p
					curHighBet = tpl[p].remainingBet
					count = 1
					while i < playerCount-1:
						if tpl[p].finalScore == tpl[i+1].finalScore:
							if curHighBet < tpl[i+1].remainingBet:
								curHighBet = tpl[i+1].remainingBet
							count+=1
						else:
							break
						i+=1
					
					i = 0
					curTotalBet = 0
					while i < count:
						if curHighBet <= tpl[p+i].remainingBet:
							curTotalBet+=curHighBet
						else:
							curTotalBet+=tpl[p+i].remainingBet
						i+=1

					i = 0
					totalRemBet = 0
					while (p+i) < playerCount:
						if curHighBet <= tpl[p+i].remainingBet:
							totalRemBet+=curHighBet
						else:
							totalRemBet+=tpl[p+i].remainingBet
						i+=1

					try:
						mulFac = totalRemBet/curTotalBet
					except:
						mulFac = 0
					i = 0
					while i < count:
						winAmt = round(tpl[p+i].remainingBet * mulFac)
						if winAmt > 0:
							tpl[p+i].money += winAmt
							print("	{:<8} has won ${}  with {} = {}".format(tpl[p+i].name,winAmt,self.pokerHands(tpl[p+i].handScore),tpl[p+i].finalHand))
						i+=1

					i = 0
					while (p+i) < playerCount:
						if curHighBet <= tpl[p+i].remainingBet:
							tpl[p+i].remainingBet -= curHighBet
						else:
							tpl[p+i].remainingBet = 0
						i+=1

					p = p + count

			p = 0
			while p < playerCount:
				players[p].money+=players[p].remainingBet
				p+=1
			# unpacking players list order
			i = 0
			while i < playerCount:
				players[i] = playersDict[i]
				i+=1

		else:
			for each in players:
				if not each.fold:
					each.money = each.money + round(self.pot)
					print(f"\n {each.name} has won ${round(self.pot)}")


class player():
	def __init__(self, name, money = 1000):
		self.name = name
		self.money = money
		self.check = False
		self.cards = []
		self.currentBet = 0
		self.totalBet = 0
		self.fold = False
		# handAttributes i, j, stCount, isFlush [first card count, second card count, no of straight cards, isFlush]
		self.handAttributes = [1,1,1,""]
		self.handScore = 0
		self.finalHand = []
		self.finalScore = 0
		self.remainingBet = 0

	def resetPlayer(self):
		self.check = False
		self.cards = []
		self.currentBet = 0
		self.totalBet = 0
		self.fold = False
		self.handAttributes = [1,1,1,""]
		self.handScore = 0
		self.finalHand = []
		self.finalScore = 0
		self.remainingBet = 0

def countOfPlayers(players):
	p = 0
	for each in players:
		if not each.fold and each.money > 0:
			p+=1
	return p

def betting(bettingType = "Regular"):
	for each in players:
		each.check = False
	if bettingType == "Initial":
		betStartPosition = (dealer.dealPosition+1) % playerCount
	else:
		betStartPosition = (dealer.dealPosition + playerCount -1) % playerCount

	playPosition = betStartPosition
	currentPlayer = players[playPosition % playerCount]

	while playerCount - dealer.foldPlayerCount != 1:
		if not currentPlayer.fold:
			if currentPlayer.money > 0:
				choice = dealer.getChoice(currentPlayer)
				# choice = "2"
				dealer.doChoice(currentPlayer, choice)
		
		playPosition+=1
		currentPlayer = players[playPosition % playerCount]

		if currentPlayer.currentBet == dealer.currentBet or currentPlayer.fold or currentPlayer.money == 0:
			if playPosition % playerCount == betStartPosition:
				dealer.currentBet = 0
				for each in players:
					each.currentBet = 0
				break

def gameStart(dealer,players):
	clear()
	global playerCount
	for each in players:
		if each.money <= 1:
			players.pop(players.index(each))
	playerCount = len(players)
	if playerCount <= 1:
		clear()
		print("\n			...~~~|!|>---<__ BoomPa's CASINO __>---<|!|~~~... ")
		input(f"\n\n\n\n\n 			{players[0].name} has won the game.")
		exit()
	dealer.resetDeck()
	for each in players:
		each.resetPlayer()
	dealer.takeBlinds()
	dealer.dealCards()
	betting("Initial")
	dealer.flop()
	if countOfPlayers(players) > 1:
		betting()
	dealer.turn()
	if countOfPlayers(players) > 1:
		betting()
	dealer.river()
	if countOfPlayers(players) > 1:
		betting()
	dealer.sayWinner()
	print("\n\n")
	for each in players:
		print("\n  {:<8}  ${:<6} 	{} 	{} = {}".format(each.name,each.money,each.cards,each.finalHand,dealer.pokerHands(each.handScore)))
	input()
	gameStart(dealer,players)

if __name__ == "__main__":
	playerCount = int(input("No of Players: "))
	if playerCount < 2 or playerCount > 9:
		print("\n\n 	Nope. Byye!\n\n")
		exit()

	players = ["player"] * playerCount
	for each in players:
		name = input(f"Name of Player {players.index(each)+1}:  ")
		players[players.index(each)] = player(name.title())
	dealer = deck()
	gameStart(dealer,players)