import random
from os import system
import time
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
replay=True
playing=True

class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.all_cards=[]
        for suit in suits:
            for rank in ranks:
                # Create the Card Object
                created_card=Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self,who):

        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        self.who=who

    def __str__(self):
        return self.who

    def add_card(self,card):
        self.cards.append(card)
        if card.rank=='Ace':
            self.aces+=1
        self.value+=card.value
        #print(f'Current value of hand: {self.value}')
        #print(f'{card} added to hand')

    def adjust_for_ace(self):
        #if self.value>21 and self.aces!=0:
        for adjust in range(self.aces):
            self.value-=10
            if self.value<21:
                self.aces-=1
                break

class Chips:

    def __init__(self,amount):
        self.total = amount
        self.bet = 0

    def win_bet(self):
        self.total+=self.bet

    def lose_bet(self):
        self.total-=self.bet

    def take_bet(self):
        while True:
            try:
                self.bet=int(input("Your bet: $"))
                if self.bet<=self.total:
                    break
                else:
                    print(f'Insufficient funds. Available balance is ${self.total}')
            except:
                print("\nUser entry not an integer")
                print("Please try again\n")

def show_some(hand):
    print('\n--Hidden!-',end='')
    for i in range(1,len(hand.cards)):
        print(f'-{hand.cards[i]}-',end='')
    print('\n')

def show_all(hand):

    for card in hand.cards:
        print(f'-{card}-',end='')
    print(f'\n\nTotal value in hand = {hand.value}')

def hit(deck,hand):
    hand.add_card(deck.deal())
    if hand.value>21 and hand.aces!=0:
        hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    while True:
        print(f'\n{hand}')
        move=input("Your move - Hit or Stand?: ").lower()
        if move=='hit' or move=='h':
            hit(deck,hand)
            break
        elif move=='stand' or move=='s':
            print("\nPlayer Stands. Dealer's turn...")
            time.sleep(2)
            playing=False
            break
        else:
            print('\nInvalid move - Please choose Hit or Stand')

def win_scenarios(hand1,hand2,bank):
    if hand1.value>21:
        print(f"\n{hand1}'s hand exceeds 21! {hand1} busts!")
        bank.lose_bet()
    elif hand2.value>21:
        print(f"\n{hand2}'s hand exceeds 21! {hand2} busts!")
        bank.win_bet()
    elif hand1.value>hand2.value and hand1.value<=21:
        print(f"\n{hand1} beats {hand2}!")
        bank.win_bet()
    elif hand1.value<hand2.value and hand2.value<=21:
        print(f"\n{hand2} beats {hand1}!")
        bank.lose_bet()
    else:
        print(f"\nBoth hands tied in value. {hand1} receives the bet back")

def replay():
    global replay,playing
    while True:
        play_again=input('\nDo you want to play again - Y or N?: ').lower()
        if play_again=='y':
            playing=True
            break
        elif play_again=='n':
            replay=False
            break
        else:
            print("\nEnter Y or N")
    time.sleep(1)
    system('clear')

print("\n"+"*"*20)
print("WELCOME TO BLACKJACK")
print("*"*20+"\n")

# Set up player bank
while True:
    try:
        amount=int(input("\nHow many dollars worth chips do you need? $"))
        break
    except:
        print("\nEnter a valid amount for your bank")
player_bank=Chips(amount)

while replay:
    # Initialize deck and shuffle it
    new_deck=Deck()
    new_deck.shuffle()

    # Take player bet
    player_bank.take_bet()

    # Deal the first 2 cards to the player and dealer
    player_hand=Hand('Player')
    dealer_hand=Hand('Dealer')
    for x in range(2):
        player_hand.add_card(new_deck.deal())
        dealer_hand.add_card(new_deck.deal())

    while playing:
        # Show all cards for player and one card hidden for dealer
        print(f"\n{dealer_hand}'s hand:")
        show_some(dealer_hand)
        print(f"\n{player_hand}'s hand:")
        show_all(player_hand)

        # Take player's move - hit or stand
        hit_or_stand(new_deck,player_hand)

        # Check for bust and break out of playing loop if busted
        if player_hand.value>21:
            break

        system('clear')

        # Dealer plays once player calls "stand" and is not busted
        if playing==False:
            while True:
                if dealer_hand.value>=17:
                    break
                hit(new_deck,dealer_hand)

    # Shows both hands once both players are done with their moves
    system('clear')
    print(f"\n{dealer_hand}'s hand:")
    show_all(dealer_hand)
    print(f"\n{player_hand}'s hand:")
    show_all(player_hand)

    # Compute win scenarios
    print("\n"+"*"*20)
    win_scenarios(player_hand,dealer_hand,player_bank)
    print("*"*20+"\n")

    print(f'\nYour chips total after last game: ${player_bank.total}')

    # Check for player bankruptcy
    if player_bank.total==0:
        print('\nYour chips are finished. Ending game...')
        break

    # Ask for playing game again
    replay()

print(f'\nThank you for playing! Your final chips total is ${player_bank.total}')
exit()
