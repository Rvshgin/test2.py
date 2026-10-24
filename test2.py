import random
import time
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, cordinate, health, stamina, facing):
        self.cordinate = cordinate
        self.health = health
        self.stamina = stamina
        self.facing = facing
        

    @property
    def is_dead(self):
        return self.health == 0
    
    @property
    def stamina(self):
        return self.__stamina
    @stamina.setter
    def stamina(self, value):
        if 0 <= value <= 20:
            self.__stamina = value
        elif type(value) != int:
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
        return self.__health
    @health.setter
    def health(self, value):
        if 0 <= value <= 20:
            self.__health = value
        elif type(value) != int:
            raise TypeError
        else:
            raise ValueError
        
    @property
    def facing(self):
        return self.__facing
    @facing.setter
    def facing(self, value):
        if type(value) != str:
            raise ValueError
        self.__facing = value

    
                

    @abstractmethod
    def attack(self):
        pass
    @abstractmethod
    def heal(self):
        pass
   
    def move_forward(self):

        if self.stamina > 0:
            if self.facing == "south":
                self.cordinate[2] -= 1
                self.distance_from_home += 1
            elif self.facing == "north":
                self.cordinate[2] += 1
                self.distance_from_home += 1
            elif self.facing == "east":
                self.cordinate[0] += 1
                self.distance_from_home += 1
            elif self.facing == "west":
                self.cordinate[0] -= 1
                self.distance_from_home += 1

                print("moving forward")                    
            try:
                self.stamina -= 1
            except ValueError as e:
                print(e)
            
    def move_backward(self):
        if self.stamina > 0:
            if self.facing == "south":
                self.cordinate[2] += 1
                self.distance_from_home += 1
            elif self.facing == "north":
                self.cordinate[2] -= 1
                self.distance_from_home += 1
            elif self.facing == "east":
                self.cordinate[0] -= 1
                self.distance_from_home += 1
            elif self.facing == "west":
                self.cordinate[0] += 1
                self.distance_from_home += 1
                                                        
            print("moving backward")
            try:
                self.stamina -= 1
            except ValueError:
                print("you runs out of stamina")

    @classmethod
    def mk_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

class Logic:
    def __init__(self, player, enemy):
        self.player = player 
        self.enemy = enemy
        self.players_in_game = []
        self.enemy_list = []
        self.enemy_in_fight = None

    def main(self):
        self.connect_player()
        self.distribute_enemy()
        self.game_menu()



    def remove_enemy(self):
        for e in self.enemy_list:
            if e.is_dead:
                self.enemy_list.remove(e)









    def player_attack(self):
        self.players_in_game[0].attack(self.enemy_in_fight)
        if self.enemy_in_fight.is_dead:
            print("enemy is dead")
    def connect_player(self):
        p = self.spawn_player([0,1,0], 20, 20, "east", 5)
        self.players_in_game.append(p)
        
    def game_menu(self):
        current_player = self.players_in_game[0]
        
        while True:
            
            self.contact_with_enemy()
            
            print("health:",current_player.health, "stamina:", current_player.stamina, "cordinate:", current_player.cordinate)
            if current_player.is_dead:
                break
            i = input("!!!move!!!\n1.move forward\n2.move backward\n3.attack\n4.heal\n:")
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
        p = self.players_in_game[0]
        for e in self.enemy_list:
            if e.cordinate == p.cordinate:
                e.attack(p)
                p.move_backward()
                self.enemy_in_fight = e        
            
            
            
    def distribute_enemy(self):
         
            for _ in range(0,2):
                x = random.randint(0,3)
                z = random.randint(0,3)
                #felan mehvar z ro az kar endakhtam ta badan
                self.enemy_list.append(self.spawn_zombie([x,1,0], 10, 10, "east", 5))

    def spawn_player(self, cordinate, health, stamina, facing, attackdamage):
        return self.player.mk_instance(cordinate, health, stamina, facing, attackdamage)

    def spawn_zombie(self, cordinate, health, stamina, facing, attackdamage):
        return self.enemy.mk_instance(cordinate, health, stamina, facing, attackdamage)

class Enemmy(Entity):
    def __init__(self, cordinate, health, stamina, facing, attackdamage):
        super().__init__(cordinate, health, stamina, facing)
        self.attack_damage = attackdamage
        self.Sight = 5
        
    
    def attack(self, target):
        try:
            self.stamina -= 4
            target.health -= self.attack_damage
        except ValueError:
            print("")

    def heal(self):
        pass





class Player(Entity):
    def __init__(self, cordinate, health, stamina, facing, attackdamage):
        super().__init__(cordinate, health, stamina, facing)
        self.attack_damage = attackdamage
        
   
    def heal(self):
        try:
            self.health += 5
        except ValueError:
            print("health is full")

    def attack(self, target):
        try:
            self.stamina -= 4
            target.health -= self.attack_damage
        except ValueError:
            print("")
        
        
        

    def logic(self):
        if self.distance_from_home >= 10:
            self.enemy()
            self.end_of_game()
            self.heal_stamina()

    def end_of_game(self):
        if self.health == 0:
            self.is_dead = True

    


Logic(Player, Enemmy).main()