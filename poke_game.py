"""
Pokemon Game
"""

import time
from enum import Enum, auto


class Helpers:
    """Helper functions"""

    def multiple_choice_txt(options: list):
        """
        Show options for multiple-choice question, then validate and return input. Repeat until valid input
        is given.
        :return: index of the user response
        """

        # Show options
        for e, option in enumerate(options):
            print(f"{e}. {option}")

        # Repeat until valid response
        while True:
            try:
                i = int(input("Enter number: "))
            except ValueError:
                print("Invalid input. Please input a number.")
                continue
            else:
                if i < 0 or i >= len(options):
                    print(f"Invalid input. Please input a number between 0 and {len(options)-1}.")
                else:
                    break

        print(f"You choose {options[i]}.\n")

        return i


class Game:

    player_flag = True  # indicates if turn is about player (True) of opponent (False)
    player_index = 0  # index of the current pokemon in the player's deck
    opponent_index = 0  # index of the current pokemon in the opponent's deck

    def __init__(self, deck, opponent_deck):
        self.deck = deck
        self.opponent_deck = opponent_deck

    def _switch(self, deck):
        """ Function to switch current Pokemon
        :param deck: List of Pokemon classes
        """

        print("Pick a Pokemon")
        for e, i in enumerate(deck):  # For all Pokemon in the deck
            if i.health > 0:  # only list Pokemon that are alive
                print(f"{e}. {i.name}")
        user_input = int(input())  # todo: fix to use function multiple_choice_txt!

        # Change index depending on who is switching
        if self.player_flag:
            self.player_index = int(user_input)
            print(f"You choose {deck[self.player_index].name}.\n")
        else:
            self.opponent_index = int(user_input)
            print(f"You choose to fight {deck[self.opponent_index].name}.\n")

        # back to menu
        self.start()

    def start(self):
        """Main menu of the game."""
        # Print Game stats
        # todo: use variables instead of self.deck[self.player_index] and self.opponent_deck[self.opponent_index]
        print("-------------------------------------")
        print(f"Player 1. {self.deck[self.player_index].name} ({self.deck[self.player_index].health} HP) "
              f"and {len(self.deck)-1} other Pokemon.")
        print(f"Player 2. {self.opponent_deck[self.opponent_index].name} "
              f"({self.opponent_deck[self.opponent_index].health} HP) "
              f"and {len(self.opponent_deck)-1} other Pokemon.")
        print("-------------------------------------\n")

        # Menu
        print("What would you like to do?")
        user_input = Helpers.multiple_choice_txt(['Attack!', 'Pick opponent', 'Switch Pokemon', 'Exit'])

        # Attack
        if user_input == 0:
            # user attacks opponent
            # todo: move to separate private function
            # todo: use player_pokemon = self.deck[self.player_index]
            print(f"{self.deck[self.player_index].name} uses {self.deck[self.player_index].attack_name}!")
            self.opponent_deck[self.opponent_index].get_hurt(self.deck[self.player_index].attack_power)
            # opponent strikes back
            time.sleep(2)
            print(f"{self.opponent_deck[self.opponent_index].name} "
                  f"stikes back with {self.opponent_deck[self.opponent_index].attack_name}")
            self.deck[self.player_index].get_hurt(self.opponent_deck[self.opponent_index].attack_power)
            self.start()

        # Pick opponent
        if user_input == 1:
            self.player_flag = False
            self._switch(self.opponent_deck)

        # Switch
        if user_input == 2:
            self.player_flag = True
            self._switch(self.deck)

        # Exit
        if user_input == 3:
            exit()


class PokemonType(Enum):
    """Possible Pokemon Types"""

    GRASS = auto()
    FIRE = auto()
    WATER = auto()
    NORMAL = auto()
    ELECTRIC = auto()


class Pokemon:

    def __init__(self, name, pokemon_type: PokemonType, attack_name='bite'):
        self.name = name
        self.health = 100
        self.attack_power = 20
        self.attack_name = attack_name
        self.type = pokemon_type
        self.is_current = 0

    def get_hurt(self, attack_power_opponent):
        """Function to receive damage
        :param attack_power_opponent: attack_power of the opponent's Pokemon
        """
        print(f"{self.name} took {attack_power_opponent} damage!\n")
        self.health += -1 * attack_power_opponent


# Create a deck (list) of Pokemon:
# todo: deck to Deck Class with add_pokemon() and remove_pokemon() functions
pokedeck = [Pokemon(name='Bulbasaur', pokemon_type=PokemonType.GRASS),
            Pokemon(name='Charmander', pokemon_type=PokemonType.FIRE),
            Pokemon(name='Squirtle', pokemon_type=PokemonType.WATER),
            Pokemon(name='Rattata', pokemon_type=PokemonType.NORMAL),
            Pokemon(name='Pikachu', pokemon_type=PokemonType.ELECTRIC, attack_name='shock')]

pokedeck_opponent = [Pokemon(name='Charizard', pokemon_type=PokemonType.FIRE),
                     Pokemon(name='Raichu', pokemon_type=PokemonType.ELECTRIC)]

if __name__ == '__main__':
    print("Welcome to POKEMON")
    new_game = Game(pokedeck, pokedeck_opponent)
    new_game.start()


# todo: Possibility for dying pokemon: health goes negative without consequences
# todo: Possibility to win a game
