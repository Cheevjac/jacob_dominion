
default_2_player_base = {
            "Curse": 10,
            "Estate": 8,
            "Duchy": 8,
            "Province": 8,
            "Copper": 46, 
            "Silver": 40,
            "Gold": 30
        }

default_3_player_base = {
            "Curse": 20,
            "Estate": 12,
            "Duchy": 12,
            "Province": 12,
            "Copper": 39, 
            "Silver": 40,
            "Gold": 30
        }

default_4_player_base = {
            "Curse": 30,
            "Estate": 12,
            "Duchy": 12,
            "Province": 12,
            "Copper": 32, 
            "Silver": 40,
            "Gold": 30
        }

class GameBoard:
    def __init__(self, num_players, base_card_names, kingdom_card_names):
        self.num_players = num_players

        self.base_piles = {}
        self.kingdom_piles = {}

        self.initialize_piles(base_card_names, kingdom_card_names)

    def initialize_piles(self, base_card_names, kingdom_card_names):
        base_card_count = default_2_player_base
        if self.num_players == 3:
            base_card_count = default_3_player_base
        elif self.num_players == 4:
            base_card_count = default_4_player_base

        for card_name in base_card_names:
            if card_name in base_card_count:
                self.base_piles[card_name] = base_card_count[card_name]
            else:
                print(f"Unknown base card: {card_name}")
        
        for card_name in kingdom_card_names:
            self.kingdom_piles[card_name] = 10  # Default number for kingdom cards

    def show_board(self):
        """Display the current state of the board."""
        print(f"\nNumber of players: {self.num_players}")
        
        print("\nBase Card Piles:")
        for card_name, count in self.base_piles.items():
            print(f"{card_name}: {count} cards")
        
        print("\nKingdom Card Piles:")
        for card_name, count in self.kingdom_piles.items():
            print(f"{card_name}: {count} cards")

    def draw_card_from_pile(self, card_name):
        """Draw a card from the base or kingdom pile, automatically checking both."""
        
        # Check if the card is in the base piles
        if card_name in self.base_piles:
            self.base_piles[card_name] -= 1
            print(f"Drew a {card_name} from base pile. Cards left: {self.base_piles[card_name]}")

        # Check if the card is in the kingdom piles
        elif card_name in self.kingdom_piles:
            self.kingdom_piles[card_name] -= 1
            print(f"Drew a {card_name} from kingdom pile. Cards left: {self.kingdom_piles[card_name]}")

        # If card is not found in either pile
        else:
            print(f"{card_name} not found in any pile.")
            return False

    def cards_available(self):
        available_cards = []
        for card, count in self.base_piles.items():
            if (count > 0):
                available_cards.append(card)
        
        for card, count in self.kingdom_piles.items():
            if (count > 0):
                available_cards.append(card)
        return available_cards
            
        