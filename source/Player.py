import random
class Player:
    def __init__(self, name):
        self.name = name
        self.buy_power = 0
        self.actions = 0
        self.buys = 0
        self.hand = []
        self.discard_pile = []
        self.deck = []

    def shuffle_in_discard(self):
        """Shuffle all cards in discard, add them to deck, and remove from discard"""
        random.shuffle(self.discard_pile)
        self.deck.extend(self.discard_pile)
        self.discard_pile = []

    def discard_cards(self, card_indices):
        """Remove cards from hand based on an array of indices and add them to discard pile"""
        # Sort the indices in descending order to avoid index shifting issues during removal
        card_indices = sorted(card_indices, reverse=True)
        
        for card_index in card_indices:
            if 0 <= card_index < len(self.hand):
                card = self.hand.pop(card_index)
                self.discard_pile.append(card)
            else:
                print(f"Invalid index: {card_index}. No card discarded for this index.")


    def draw_card(self, count, to_hand = True):
        """Draw a card from the deck and add it to the hand"""
        drawn = []
        for _ in range(count):
            if not self.deck:
                self.shuffle_in_discard()
                print("Deck is empty, Shuffling in Discard.")

            card = self.deck.pop(0)
            if to_hand:
                self.hand.append(card)
            else:
                drawn.append(card)
        return drawn
            
    def reset_turn(self):
        """Reset actions, buys, and buying power at the start of the turn discard cards and draw"""
        self.actions = 1
        self.buys = 1
        self.buy_power = 0
        
        self.discard_pile.extend(self.hand)
        self.hand = []

        self.draw_card(5)



