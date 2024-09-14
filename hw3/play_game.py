from week2_classes_objects.hw3.DeckOfCards import *

print("Welcome to BlackJack!")

deck = DeckOfCards()
deck.print_deck()
deck.shuffle_deck()
deck.print_deck()

def calculate_score(cards):
    score = 0
    aces = 0
    for card in cards:
        score+=card.value
        if card.face == 'Ace':
            aces+=1

    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score

# deal two cards to the user
card = deck.get_card()
card2 = deck.get_card()
player_hand = [card, card2]
score = calculate_score(player_hand)

print("Your cards: ", card, card2)
print("Your score is: ", score)

dealer_card = deck.get_card()
dealer_card2 = deck.get_card()
dealer_hand = [dealer_card, dealer_card2]
dealer_score = calculate_score(dealer_hand)

print("Dealers visible card:", dealer_card)

hit = input("Would you like a hit? (y/n):").lower()

while hit == 'y':
    card3 = deck.get_card()
    player_hand.append(card3)
    score = calculate_score(player_hand)
    print("You got:", card3)
    print("New score: ", score)

    if score > 21:
        print("Busted! Game over.")
        exit()
    
    hit = input("Would you like another hit? (y/n): ").lower()

print("Dealers hidden card was: ", dealer_card2)
print("Dealers initial score: ", dealer_score)

while dealer_score < 17:
    print("Dealer hits")

    if len(deck.deck) == 0:
        print("No more cards in the deck!")
        exit()
    
    dealer_card3 = deck.get_card()
    dealer_hand.append(dealer_card3)
    dealer_score = calculate_score(dealer_hand)
    print("Dealer got: ", dealer_card3)
    print("Dealer score: ", dealer_score)

print("\nFinal Scores: \nYour score: ", score, "\nDealer's Score: ", dealer_score)

if dealer_score > 21:
    print("Dealer busted! You win!")
elif score > dealer_score:
    print("You win!")
elif score < dealer_score:
    print("Dealer wins")
else:
    print("Tie")
