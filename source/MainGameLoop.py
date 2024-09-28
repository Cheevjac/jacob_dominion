import json
from Player import Player
from GameBoard import GameBoard

players = []
game_board = None


with open('resources/cards.json', 'r') as file:
    card_data = json.load(file)

def get_player_input(query, valid_min, valid_max, card_list):
    help_message = f"""
    Help:
    - Type -h or -help for this help message.
    - Type "-c card_name" for information on card.
    - Enter a space-separated list of numbers (for card positions) or card names.
    - The length of the list should be between {valid_min} and {valid_max}.
    - Card numbers must be between 0 and {len(card_list) - 1}.
    """
    
    while True:
        # Print the query and the card list in the required format
        user_input = input(f"{query} {card_list_to_string(card_list)}: ")

        # Check if user asked for help
        if user_input.lower() in ['-h', '-help']:
            print(help_message)
            continue  # Repeat the query after showing help message

        # Check if the user asked for card details
        if user_input.lower().startswith('-c '):
            card_name = user_input[3:].strip()  # Extract card name after "-c"
            if card_name in card_data:
                card = card_data[card_name]
                print(f"Name: {card_name}\nCost: {card['cost']}\nDescription: {card['text']}")
            else:
                print(f"{card_name} is not a valid card name.")
            continue  # Repeat the query after showing card details

        # Parse the space-separated list of inputs (can be numbers or card names)
        input_items = user_input.split()

         # Check if the length is within the valid range
        if not valid_min <= len(input_items) <= valid_max:
            print(f"Invalid input. Please enter a list of {valid_min} to {valid_max} items.")
            continue

        # Check if the input contains valid card names or indices
        valid_indices = []
        for item in input_items:
            # Check if item is a number and within the range of card_list
            if item.isdigit():
                num = int(item)
                if 0 <= num < len(card_list):
                    valid_indices.append(num)  # Append the index (number)
                else:
                    print(f"Invalid input. Card number {num} is out of range.")
                    break
            # Otherwise, treat the item as a card name and find its index
            elif item in card_list:
                valid_indices.append(card_list.index(item))  # Append the index of the card name
            else:
                print(f"Invalid input. {item} is neither a valid card number nor a valid card name.")
                break
        else:
            # If all inputs are valid, return the valid indices
            return valid_indices


def card_list_to_string(card_names):
    # Use list comprehension to create the formatted string for each card with index
    formatted_cards = [f"{i} - {card}" for i, card in enumerate(card_names)]
    return ", ".join(formatted_cards)

def simple_card_to_string(card_names):
    formatted_cards = [f"{card}" for i, card in enumerate(card_names)]
    return ", ".join(formatted_cards)

def get_cards_under_price(price):
    under_price = []
    available_cards = game_board.cards_available()
    for card_name in available_cards:
        if card_data[card_name]["cost"] < price:
            under_price.append(card_name)
    return under_price

def get_other_players(player):
    return [p for p in players if p != player]

def get_cards_of_type(card_list, desired_type):
        return [card for card in card_list if card_data[card]["type"] == desired_type]


def move_lists_by_index(source_list, target_list, indices):
    # Sort indices in descending order to avoid shifting issues
    indices = sorted(indices, reverse=True)

    for index in indices:
        if 0 <= index < len(source_list):
            # Pop from source and append to target
            item = source_list.pop(index)
            target_list.insert(0, item)


def score_deck(deck):
    vp = 0
    card_count = 0
    Gardens_count = 0
    for card in deck:
        card_count += 1
        if card == "Garden":
            Gardens_count += 1
        elif card == "Curse":
            vp -= 1
        elif card == "Estate":
            vp += 1
        elif card == "Duchy":
            vp += 3
        elif card == "Province":
            vp += 8
    
    vp += int(Gardens_count*(card_count/10))
    return vp

def main_game_loop():
    print("Welcome to Jacob's version of the game Dominion!")
    instructions = """
    Instructions:
    When prompted to select cards out of a hand or discard you will be given a list of cards that looks like
    1 - card1, 2 - card2, 3 - card3, etc...
    To select a card or cards enter your selection as a space seperated list of numbers. 
    If you need help at any time just type -h.
    If you need details on a card just type -c card_name.
    """
    print(instructions)
    
    # Get player information
    query = 'Please select the number of players'
    player_count_options = ['zero', 'one', 'two', 'three', 'four']
    response = get_player_input(query, 0, 1, player_count_options)
    num_players = response[0]
    if num_players == 0:
        print('Zero Players means Zero Game!')
        return

    for i in range(num_players):
        player_name = input(f"Enter the name of player {i + 1}: ")
        players.append(Player(player_name))
    
    # Get the kingdom card names
    base_cards = ["Curse", "Estate", "Duchy", "Province", "Copper", "Silver", "Gold"]
    kingdom_cards = ["Cellar", "Council_Room", "Smithy", "Throne_Room", "Vassal", "Village", "Workshop", "Festival", "Harbinger", "Market"]
    
    # print("Enter 10 kingdom card names (one per line):")
    # for i in range(10):
    #     kingdom_card = input(f"Kingdom card {i + 1}: ")
    #     kingdom_cards.append(kingdom_card)
    
    # Instantiate the game board
    global game_board
    game_board = GameBoard(num_players, base_cards, kingdom_cards)
    
    # Give players initial cards
    initial_cards = ["Copper", "Copper", "Copper", "Copper", "Copper", "Copper", "Copper", "Estate", "Estate", "Estate"]
    for player in players:
        player.discard_pile.extend(initial_cards)
        player.reset_turn()
    # Game loop
    game_over = False
    turn_counter = 0
    
    while not game_over:
        print(f"\n=== Turn {turn_counter + 1} ===")
        
        # Loop through each player's turn
        for player in players:
            print(f"{player.name}'s turn:")
            player_pass = False
            while(not player_pass):
                status = "\n--- " + player.name + "'s play ---\nHand: " + simple_card_to_string(player.hand) + "\nActions: " + str(player.actions)
                status += ", Buys: " + str(player.buys) + ", Buy Power: " + str(player.buy_power)
                query = status + "\nPlease select an option:"
                options = ["Play_Action", "Buy_Card", "Show_Board", "Play_All_Treasure", "Pass"]
                response = get_player_input(query, 1, 1, options)
                if (response[0] == 0):
                    if player.actions > 0:
                        query = player.name + ":\nPlease select a card to play"
                        response = get_player_input(query, 0, 1, player.hand)
                        card_name = player.hand[response[0]]
                        card_type = card_data[card_name]["type"]
                        if(card_type == "action" or card_type == "action-attack"):
                            player.actions -= 1
                        player.discard_cards([player.hand.index(card_name)])
                        play_card(card_name, player)
                        
                elif (response[0] == 1): 
                    query = player.name + ":\nPlease select a card to buy"
                    buy_options = get_cards_under_price(player.buy_power)
                    response = get_player_input(query, 0, 1, buy_options)
                    if response:
                        card_name = buy_options[response[0]]
                        game_board.draw_card_from_pile(card_name)
                        player.discard_pile.append(card_name)
                        player.buys -= 1
                        player.buy_power -= card_data[card_name]["cost"]
                
                elif (response[0] == 2):
                    game_board.show_board()

                elif (response[0] == 3):
                    treasure_indices = [i for i, card in enumerate(player.hand) if card_data[card]["type"] == "treasure"]
                    treasure_names = [card for card in player.hand if card_data[card]["type"] == "treasure"]
                    player.discard_cards(treasure_indices)
                    for card_name in treasure_names:
                        play_card(card_name, player)
                    
                
                elif (response[0] == 4):
                    player_pass = True
                
            
            # Reset player's turn
            player.reset_turn()
        
        # Check end condition (e.g., if 3 piles are empty)
        empty_piles = 0
        for pile in game_board.kingdom_piles.values():
            if pile == 0:
                empty_piles += 1
        
        if empty_piles >= 3:
            game_over = True
            print("Game over! Too many empty piles.")

        if game_board.base_piles["Duchy"] == 0 or game_board.base_piles["Province"] == 0:
            game_over = True
            print("Game over! Duchy or Province pile empty.")
        
        turn_counter += 1
    
    max_score = 0
    max_player = ""
    for player in players:
        player.discard_pile.extend(player.cards_in_hand)
        player.cards_in_hand = []
        player.shuffle_in_discard()
        print(f"\n{player.name}'s final deck:")
        string_card_list = simple_card_to_string(player.deck)
        print(string_card_list)
        player_score = score_deck(player.deck)
        print(f"\n{player.name}'s score: {player_score}")
        if player_score > max_score:
            max_score = player_score
            max_player = player.name
        
    print(f"The winner is {max_player} with a score of {max_score}.")
    print("Thanks for playing!")

# Start the game
main_game_loop()

def play_card(card_name, player, special="none"):
    card = card_data[card_name]
    if card["type"] == "victory":
        print("Victory cards can't be played!")
        return
    if card["type"] == "curse":
        print("Curse type cards can't be played!")
        return

    match card_name:
        case "Copper":
            player.buy_power += 1

        case "Silver":
            player.buy_power += 2
            if special == "Merchant":
                player.buy_power += 1

        case "Gold":
            player.buy_power += 3

        case "Artisan":
            under_price = get_cards_under_price(5)
            query = player.name + ":\nplease select a card to add to your hand."
            response = get_player_input(query, 1, 1, under_price)
            card_name = under_price[response[0]]
            game_board.draw_card_from_pile(card_name)
            player.hand.extend(card_name)
            query = player.name +":\nplease select a card to put on top of your deck"
            response = get_player_input(query, 1, 1, player.hand)
            move_lists_by_index(source_list=player.hand, target_list=player.deck, indices=response)

        case "Bandit":
            game_board.draw_card_from_pile('Gold')
            player.discard_pile.append('Gold')
            other_players = get_other_players
            for other_player in other_players:
                top_cards = other_player.draw_card(2, False)
                for card_name in top_cards:
                    if card_data[card_name]["type"] == "treasure" and card_name != 'Copper':
                        print(f'{other_player.name} revealed a {card_name} -> trashing.')
                    else:
                        print(f'{other_player.name} revealed a {card_name} -> discardings.')
                        other_player.discard.append(card_name)

        case "Bureaucrat":
            game_board.draw_card_from_pile('Silver')
            player.deck.insert(0,'Silver')
            other_players = get_other_players(player)
            for other_player in other_players:
                victory_cards = get_cards_of_type(other_player.hand, 'victory')
                if victory_cards:
                    query = other_player.name + ":\nPlease select a victory card to put on your deck"
                    response = get_player_input(query, 1, 1, victory_cards)
                    move_lists_by_index(source_list=victory_cards, target_list=other_player.deck, indices=response)
                else:
                    print(f'{other_player.name}: revealed their hand')
                    print(simple_card_to_string(other_player.hand))

        case "Cellar":
            player.actions += 1
            query = player.name + ":\nDiscard any number of cards then draw that many."
            response = get_player_input(query, 0, len(player.hand), player.hand)
            count = len(response)
            player.discard_cards(response)
            player.draw_card(count)
        
        case "Chapel":
            query = player.name + ":\nPlease select up to 4 cards to trash"
            response = get_player_input(query, 0, 4, player.hand)
            move_lists_by_index(source_list=player.hand, target_list=game_board.trash, indices=response)

        case "Council Room":
            player.draw_card(4)
            player.buys += 1
            other_players = get_other_players(player)
            for other_player in other_players:
                other_player.draw_card(1)

        case "Festival":
            player.actions += 2
            player.buys += 1
            player.buy_power += 2

        case "Harbinger":
            player.draw_card(1)
            player.actions += 1
            query = player.name + ":\nPlease select up to one card from the discard to put on deck."
            response = get_player_input(query, 0, 1, player.discard_pile)
            move_lists_by_index(source_list=player.discard_pile, target_list=player.deck, indices=response)

        case "Laboratory":
            player.draw_card(2)
            player.actions += 1

        case "Library":
            while len(player.hand) <= 7:
                card_name = player.draw_card(1, False)[0]
                print(Player.name + " drew {card_name}")
                if card_data[card_name]["type"].contains("action"):
                    options = ['yes', 'no']
                    query = player.name + f":\nKeep the action card {card_name}?"
                    response = get_player_input(query, 1, 1 options)
                    if response[0] == 0:
                        player.hand.append(card_name)
                    else:
                        player.discard_pile.append(card_name)
                else:
                    player.hand.append(card_name)

        case "Market":
            player.draw_card(1)
            player.actions += 1
            player.buys += 1
            player.buy_power += 1

        case "Merchant":
            player.draw_card(1)
            player.actions(1)
            #TODO implement the wierd silver thing

        case "Militia":
            
            
        case "Smithy":
            player.draw_card(3)
        
        case "Throne Room":
            query = player.name + ":\nPlease select an action to play twice."
            response = get_player_input(query, 1, 1, player.hand)
            card = player.hand[response[0]]
            play_card(card, player)
            play_card(card, player, "Throne_Room")
            player.actions += 2
        
        case "Vassal":
            player.buy_power += 2
            #TODO finish implementing this card

        case "Village":
            player.draw_card(1)
            player.actions(2)

        case "Workshop":
            under_price = get_cards_under_price(4)
            query = player.name +":\nPlease select a card to gain."
            response = get_player_input(query, 1, 1, under_price)
            card = under_price[response[0]]
            game_board.draw_card_from_pile(card)
            player.discard_pile.append(card)

        case "Woodcutter":
            player.buys += 1
            player.buy_power += 2