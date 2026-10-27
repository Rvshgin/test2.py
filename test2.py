"""
a program that simulates a simple game where a player can move, attack,\
and heal while facing enemies.The player and enemies have health and stamina attributes,\
and the game logic handles interactions between them.
"""

import random
import time
from abc import ABC, abstractmethod


class Entity(ABC):
    """
    An abstract base class representing a game entity\
    with attributes for coordinates, health, stamina, and facing direction.
    """

    def __init__(self, cordinate, health, stamina, facing):
        self.cordinate = cordinate
        self.health = health
        self.stamina = stamina
        self.facing = facing

    @property
    def is_dead(self):
        """
        returns True if the entity's health is 0, indicating that it is dead.
        """
        return self.health == 0

    @property
    def stamina(self):
        """
        Returns the current stamina of the entity."""
        return self.__stamina

    @stamina.setter
    def stamina(self, value):
        """
        Sets the stamina of the entity, ensuring it is within the valid range (0 to 2-0).
        """
        if 0 <= value <= 20:
            self.__stamina = value
        elif isinstance(value, str):
            raise TypeError
        else:
            raise ValueError
        if self.stamina <= 10:
            print("Exasted healing...")
            while self.stamina != 20:
                time.sleep(0.5)
                self.stamina += 1

    @property
    def health(self):
        """
        Returns the current health of the entity."""
        return self.__health

    @health.setter
    def health(self, value):
        """
        Sets the health of the entity, ensuring it is within the valid range (0 to 20).
        """
        if 0 <= value <= 20:
            self.__health = value
        elif isinstance(value, str):
            raise TypeError
        else:
            raise ValueError

    @property
    def facing(self):
        """
        Returns the current facing direction of the entity.
        """
        return self.__facing

    @facing.setter
    def facing(self, value):
        """
        Sets the facing direction of the entity, ensuring it is a string.
        """
        if isinstance(value, str):
            raise ValueError
        self.__facing = value

    @abstractmethod
    def attack(self, target):
        """
        An abstract method that must be implemented by subclasses\
        to define the attack behavior of the entity.
        """

    @abstractmethod
    def heal(self):
        """
        An abstract method that must be implemented by\
        subclasses to define the healing behavior of the entity.
        """

    def move_forward(self):
        """
        Moves the entity forward in the direction\
        it is facing, reducing stamina by 1.
        """

        if self.stamina > 0:
            if self.facing == "south":
                self.cordinate[2] -= 1

            elif self.facing == "north":
                self.cordinate[2] += 1

            elif self.facing == "east":
                self.cordinate[0] += 1

            elif self.facing == "west":
                self.cordinate[0] -= 1

                print("moving forward")
            try:
                self.stamina -= 1
            except ValueError as e:
                print(e)

    def move_backward(self):
        """
        Moves the entity backward in the direction it is facing, reducing stamina by 1.
        """
        if self.stamina > 0:
            if self.facing == "south":
                self.cordinate[2] += 1

            elif self.facing == "north":
                self.cordinate[2] -= 1

            elif self.facing == "east":
                self.cordinate[0] -= 1

            elif self.facing == "west":
                self.cordinate[0] += 1

            print("moving backward")
            try:
                self.stamina -= 1
            except ValueError:
                print("you runs out of stamina")

    @classmethod
    def mk_instance(cls, *args, **kwargs):
        """
        A class method that creates an instance of the class\
        with the provided arguments and keyword arguments.
        """
        return cls(*args, **kwargs)


class Logic:
    """
    A class that manages the game logic,\
    including player and enemy interactions, movement, and combat.
    """

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.players_in_game = []
        self.enemy_list = []
        self.enemy_in_fight = None

    def main(self):
        """
        The main method that initializes the game by connecting the player.
        """
        self.connect_player()
        self.distribute_enemy()
        self.game_menu()

    def remove_enemy(self):
        """
        Removes dead emnemies from the enemy list.
        """
        for e in self.enemy_list:
            if e.is_dead:
                self.enemy_list.remove(e)

    def player_attack(self):
        """
        Performs an attack by the player on the enemy in\
        fight and checks if the enemy is dead.
        """
        self.players_in_game[0].attack(self.enemy_in_fight)
        if self.enemy_in_fight.is_dead:
            print("enemy is dead")

    def connect_player(self):
        """
        Connects a player to the game by spawning a new player \
        instance and adding it to the players_in_game list.
        """
        p = self.spawn_player([0, 1, 0], 20, 20, "east", 5)
        self.players_in_game.append(p)

    def game_menu(self):
        """
        The main game loop that handles player actions,\
        enemy interactions, and game state updates.
        """
        current_player = self.players_in_game[0]

        while True:

            self.contact_with_enemy()

            print(
                "health:",
                current_player.health,
                "stamina:",
                current_player.stamina,
                "cordinate:",
                current_player.cordinate,
            )
            if current_player.is_dead:
                break
            i = input(
                "!!!move!!!\n1.move forward\n2.move backward\n3.attack\n4.heal\n:"
            )
            if i == "1":
                current_player.move_forward()

            elif i == "2":
                current_player.move_backward()

            elif i == "3":
                self.player_attack()
            elif i == "4":
                current_player.heal()
            else:
                break
            self.remove_enemy()

    def contact_with_enemy(self):
        """
        Checks for contact between the player and enemies,\
        and if an enemy is in the same coordinate as the player,\
        it attacks the player and moves the player backward.
        """
        p = self.players_in_game[0]
        for e in self.enemy_list:
            if e.cordinate == p.cordinate:
                e.attack(p)
                p.move_backward()
                self.enemy_in_fight = e

    def distribute_enemy(self):
        """
        Distributes enemies in the game by spawning\
        a specifid number of enemies at random coordinates,
        and adding them to the enemy_list."""
        for _ in range(0, 2):
            x = random.randint(0, 3)
            z = random.randint(0, 3)
            # felan mehvar z ro az kar endakhtam ta badan
            self.enemy_list.append(self.spawn_zombie([x, 1, 0], 10, 10, "east", 5))

    def spawn_player(self, cordinate, health, stamina, facing, attackdamage):
        """
        Spawns a new player instance with the specified attributes and returns it.
        """
        return self.player.mk_instance(cordinate, health, stamina, facing, attackdamage)

    def spawn_zombie(self, cordinate, health, stamina, facing, attackdamage):
        """
        Spawns a new enemy instance with the specified attributes and returns it."""
        return self.enemy.mk_instance(cordinate, health, stamina, facing, attackdamage)


class Enemmy(Entity):
    """
    A class representing an enemy entity in the game.
    """

    def __init__(self, cordinate, health, stamina, facing, attackdamage):
        super().__init__(cordinate, health, stamina, facing)
        self.attack_damage = attackdamage
        self.sight = 5

    def attack(self, target):
        """
        Performs an attack on the target entity, reducing the enemy's\
        stamina and the target's health by the attack damage.
        """
        try:
            self.stamina -= 4
            target.health -= self.attack_damage
        except ValueError:
            print("")

    def heal(self):
        """
        Heals the enemy by increasing its health by 5, with error handling for full health.
        """


class Player(Entity):
    """
    A class representing a player entity in the game.
    """

    def __init__(self, cordinate, health, stamina, facing, attackdamage):
        super().__init__(cordinate, health, stamina, facing)
        self.attack_damage = attackdamage

    def heal(self):
        """
        Heals the player by increasing its health by 5, with error handling for full health.
        """
        try:
            self.health += 5
        except ValueError:
            print("health is full")

    def attack(self, target):
        """
        Performs an attack on the target entity, reducing the player's\
        stamina and the target's health by the attack damage.
        """
        try:
            self.stamina -= 4
            target.health -= self.attack_damage
        except ValueError:
            print("")


Logic(Player, Enemmy).main()
