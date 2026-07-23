import random
from collections import Counter
import json
from copy import deepcopy

with open('masks.json', 'r') as file:
        SHOP_POOL = json.load(file)

with open('relics.json', 'r') as file_two:
        RELIC_POOL = json.load(file_two)

MASK_WEIGHTS = [item['weight'] for item in SHOP_POOL]
RELIC_WEIGHTS = [item['weight'] for item in RELIC_POOL]

class Dice:
    result = 0

    def __init__(self, sidesList, type, price):
        self.sides = sidesList
        self.type = type
        self.price = price

    def get_dice_info(self):
        return f"Sides: {self.sides}, Type: {self.type}, Price: {self.price}"
    
    def to_dict(self):
        info = {
            "sides": self.sides,
            "type": self.type,
            "price": self.price
        }
        return info
    
    def get_sides(self):
        return self.sides
    
    def change_sides(self, new_sides):
        self.sides = new_sides
    
    def get_type(self):
        return self.type

    def change_type(self, shell):
        self.type = shell

    def get_price(self):
        return self.price
    
    def roll_dice(self):
        self.result = random.choice(self.sides)
        return self.result
    
    def get_result(self):
        return self.result
    
DICE_POOL = [
    Dice([1, 2, 3, 4, 5, 6], "Basic", 1),
    Dice([6, 7, 8, 9, 10, 11], "Basic", 1),
    Dice([1, 1, 1, 1, 1, 1], "Basic", 1),
    Dice([2, 2, 2, 2, 2, 2], "Basic", 1),
    Dice([3, 3, 3, 3, 3, 3], "Basic", 1),
    Dice([4, 4, 4, 4, 4, 4], "Basic", 1),
    Dice([5, 5, 5, 5, 5, 5], "Basic", 1),
    Dice([6, 6, 6, 6, 6, 6], "Basic", 1),

    Dice([1, 2, 3, 4, 5, 6], "Iron", 2),
    Dice([100, 1, 100, 1, 100, 1], "Iron", 2),

    Dice([1, 2, 3, 4, 5, 6], "Gold", 2),
    Dice([1, 2, 3, 4, 5, 6], "Ivory", 2),

    Dice([1, 2, 3, 4, 5, 6], "Ruby", 2),
    Dice([10, 10, 10, 10, 10, 10], "Ruby", 2),

    Dice([1, 2, 3, 4, 5, 6], "Ethereal", 2),
    Dice([1, 2, 3, 4, 5, 6], "Poisonous", 2),
    Dice([1, 2, 3, 4, 5, 6], "Vampiric", 2),

    Dice([1, 2, 3, 4, 5, 6], "Shadow", 3),
    Dice([6, 7, 8, 9, 10, 11], "Shadow", 3),
    Dice([6, 6, 6, 6, 6, 6], "Shadow", 3),

    Dice([1, 2, 3, 4, 5, 6], "Infernal", 3),
    Dice([1, 2, 3, 4, 5, 6], "Radiant", 3)
]

DICE_WEIGHTS = [
    80, 80, 80, 80, 80, 80, 80, 80,  
    30,  30,                                 
    30,                                      
    30,                                      
    30,  30,                                 
    30,                                     
    30,
    30,
    10, 10, 10,                                      
    2,                                       
    2                                        
]
    
class Player:
    health = 100
    max_rolls = 3
    gold = 5
    dicePool = [Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1)]
    shadow_pool = []
    currentList = []
    relic_list = []
    dice_hand_modifier = 0
    gluttonous_modifier = 0

    mana = 0
    hellfire = 0

    def __init__(self):
        self.dicePool = [Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1), Dice([1, 2, 3, 4, 5, 6], "Basic", 1)]
        self.relic_list.clear()
        self.shadow_pool.clear()

    def advanced_player(self, health, max_rolls, gold, dicePool, dice_pool_mod, hellfire, shadow_pool, relic_list):
        self.health = health
        self.max_rolls = max_rolls
        self.gold = gold
        self.dicePool = dicePool
        self.dice_pool_modifier = dice_pool_mod
        self.shadow_pool = shadow_pool
        self.hellfire = hellfire
        self.relic_list = relic_list

    def view_dice_pool(self):
        count = 0
        for dice in self.dicePool:
            count += 1
            print (f"{count}. {dice.get_dice_info()}")

        count = 0
        if(len(self.shadow_pool) > 0):
            print("Shadow Dice: ")
            for dice in self.shadow_pool:
                count += 1
                print (f"{count}. {dice.get_dice_info()}")


    def add_to_dice_pool(self, dice):
        self.dicePool.append(dice)

    def get_dice_pool(self):
        return self.dicePool
    
    def set_dice_pool(self, list):
        self.dicePool = list

    def get_overview(self):
        return f"Health: {self.health}, Max Rolls: {self.max_rolls}, Gold: {self.gold}, Hand Size: {self.get_hand_size()}, Hellfire: {self.hellfire} \nRelics: {self.relic_list}"
    
    def get_money(self):
        return self.gold
    
    def set_money(self, amount):
        self.gold = amount
    
    def add_money(self, amount):
        self.gold += amount

    def calculate_interest(self):
        self.gold += self.gold // 5

    def spend_money(self, amount):
        self.gold -= amount
    
    def get_max_rolls(self):
        self.max_rolls = 3
        if(self.check_for_relic("Gambler's Glove")):
            self.max_rolls += self.gold // 10
        if(self.check_for_relic("Barbed Gauntlet")):
            self.max_rolls += 2
        if(self.check_for_relic("Bloody Blindfold")):
            self.max_rolls -= 1
        return self.max_rolls
    
    def get_current_list_from_pool(self):
        self.dice_hand_modifier = 0
        for relic in self.relic_list:
            if(relic == "Merchant's Bag"):
                self.dice_hand_modifier += self.gold // 10
            elif(relic == "Mistform Bag"):
                count = 0
                for dice in self.dicePool:
                    if(dice.get_type() == "Ethereal"):
                        count += 1
                self.dice_hand_modifier += count // 2
            elif(relic == "Bottomless Bag"):
                self.dice_hand_modifier += 3
            elif(relic == "Small Bag"):
                self.dice_hand_modifier += 1
            elif(relic == "Bloody Blindfold"):
                self.dice_hand_modifier -= 1
            elif(relic == "Braggart's Bag"):
                self.dice_hand_modifier += 1

        
        if(len(self.dicePool) >= 5 + self.dice_hand_modifier + self.gluttonous_modifier):
            self.currentList = random.sample(self.dicePool, k= 5 + self.dice_hand_modifier + self.gluttonous_modifier)
        else:
            self.currentList = random.sample(self.dicePool, k= len(self.dicePool))

        for dice in self.shadow_pool:
            self.currentList.append(dice)

    def get_current_list(self):
        return self.currentList
    
    def roll_current_list(self):
        for dice in self.currentList:
            dice.roll_dice()

    def add_shadow(self, dice):
        self.shadow_pool.append(dice)

    def get_shadow_pool(self):
        return self.shadow_pool
    
    def set_shadow_pool(self, list):
        self.shadow_pool = list

    def reroll_dice(self, indexList):
        if(self.check_for_relic("Barbed Gauntlet")):
            self.take_damage(3)

        for index in indexList:
            if(index.isdigit()):
                if(int(index) <= len(self.currentList)):
                    if(self.currentList[int(index) -1].get_type() == "Iron"):
                        pass
                    elif(self.currentList[int(index) - 1].get_type() == "Gold" and self.check_for_relic("Gilded Dagger")):
                        pass
                    elif(self.currentList[int(index) - 1].get_type() == "Infernal"):
                        self.hellfire += self.currentList[int(index) - 1].get_result()
                        self.currentList[int(index) - 1].roll_dice()
                    else:
                        self.currentList[int(index) - 1].roll_dice()
        
    
    def get_results(self):
        results_list = []
        for dice in self.currentList:
            results_list.append(dice.get_result())
        return results_list
    
    def get_roll_info(self):
        results_list = []
        for dice in self.currentList:
            results_list.append(f"{dice.get_type()}: {dice.get_result()}")
        return results_list
    
    # health ->
    def take_damage(self, amount):
        if(self.check_for_relic("Broken Buckler")):
            self.health -= (amount - 5)
        else:
            self.health -= amount

        if(self.check_for_relic("Mothbitten Cape")):
            self.gold += 2

    def heal(self, amount):
        if(self.health + amount >= 100 and self.check_for_relic("Scarlet Blade")):
            self.health += amount
        elif(self.health + amount >= 100):
            self.health = 100
        else:
            self.health += amount

    def get_health(self):
        return self.health
    
    def set_health(self, amount):
        self.health = amount
    
    def get_relic_list(self):
        return self.relic_list
    
    def add_relic(self, relic):
        self.relic_list.append(relic)

    def set_relic_pool(self, list):
        self.relic_list = list

    def add_gluttony(self):
        self.gluttonous_modifier += 1
    
    def check_for_relic(self, name):
        for relic in self.relic_list:
            if relic == name:
                return True
            
    def get_hand_size(self):
        return 5 + self.dice_hand_modifier + self.gluttonous_modifier
    
    def add_mana(self, value):
        self.mana += value

    def get_hellfire(self):
        return self.hellfire
    
    def set_hellfire(self, amount):
        self.hellfire = amount

class Monster:
    name = "Troll"
    health = 100
    damage = 10
    value = 2
    poisoned = 0

    def __init__(self):
        pass

    def advanced_monster(self, name, health, damage, value):
        self.name = name
        self.health = health
        self.damage = damage
        self.value = value

    def get_name(self):
        return self.name

    def set_health(self, amount):
        self.health = amount

    def get_health(self):
        return self.health
    
    def take_dmg(self, amount):
        self.health -= amount

    def deal_damage(self):
        return self.damage
    
    def get_value(self):
        return self.value
    
    def set_poisoned(self, value):
        self.poisoned = value

    def poison(self, value):
        self.poisoned += value

    def get_poisoned(self):
        return self.poisoned

class Game_Manager:
    dungeon = 1
    floor = 1
    round_mod = 1

    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.round_mod = 1

    def get_dungeon(self):
        return self.dungeon
    
    def get_floor(self):
        return self.floor
    
    def go_up_floor(self):
        self.monster.set_poisoned(0)
        self.floor += 1
        self.round_mod += .25
        if(self.floor == 4):
            self.go_up_dungeon()
            self.floor = 1

    def go_up_dungeon(self):
        self.dungeon += 1

    def get_round_mod(self):
        return self.round_mod
    

    def save_data(self):
        data = {
            'health': self.player.get_health(),
            'gold': self.player.get_money(),
            'dicePool': [dice.to_dict() for dice in self.player.get_dice_pool()],
            'shadowPool': [dice.to_dict() for dice in self.player.get_shadow_pool()],
            'hellfire': self.player.get_hellfire(),
            'relicPool': self.player.get_relic_list(),
            'dungeon': self.dungeon,
            'floor': self.floor,
            'round_mod': self.round_mod
        }

        return data
    
    def load_data(self, data, dice_pool, shadow_pool):
        self.player.set_health(data["health"])
        self.player.set_money(data["gold"])
        self.player.set_hellfire(data["hellfire"])
        self.player.set_dice_pool(dice_pool)
        self.player.set_shadow_pool(shadow_pool)
        self.player.set_relic_pool(data["relicPool"])
        self.dungeon = data['dungeon']
        self.floor = data['floor']
        self.round_mod = data['round_mod']

def start_of_combat_effects(player):
    for dice in player.get_current_list():
        if(dice.get_type() == "Ethereal"):
            player.get_current_list().append(Dice(dice.get_sides(), "Reflection", 1))
            if(player.check_for_relic("Haunted Robes")):
                player.get_current_list().append(Dice(dice.get_sides(), "Reflection", 1))
        elif(dice.get_type() == "Ivory"):
            if(player.check_for_relic("Cackling Skull")):
                player.get_current_list().append(Dice(dice.get_sides(), "Splinter", 1))
        elif(dice.get_type() == "Shadow" and player.check_for_relic("Smoke Veil")):
            dice.change_sides(random.choice(player.get_dice_pool()).get_sides())
    if(player.check_for_relic("Bonemarrow Flask")):
        player.get_current_list().append(Dice([1, 2, 3, 4, 5, 6], "Splinter", 1))
        player.get_current_list().append(Dice([1, 2, 3, 4, 5, 6], "Splinter", 1))

def end_of_combat_effects(player):
    for dice in player.get_dice_pool():
        if(dice.get_type() == "Gold" and player.check_for_relic("Topaz Mask")):
            player.add_money(1)
        elif(dice.get_type() == "Iron" and player.check_for_relic("Heavy Blade")):
            dice.change_sides([dice.get_sides()[0] + 5, dice.get_sides()[1] + 5, dice.get_sides()[2] + 5, dice.get_sides()[3] + 5, dice.get_sides()[4] + 5, dice.get_sides()[5] + 5])
        elif(dice.get_type() == "Infernal" and player.check_for_relic("Smoldering Robes")):
            dice.change_sides([dice.get_sides()[0] + 5, dice.get_sides()[1] + 5, dice.get_sides()[2] + 5, dice.get_sides()[3] + 5, dice.get_sides()[4] + 5, dice.get_sides()[5] + 5])
        elif(dice.get_type() == "Ruby" and player.check_for_relic("Crimson Robes")):
            player.heal(2)

    for dice in player.get_current_list():
        if(dice.get_type() == "Vampiric" and player.check_for_relic("Dracula's Eye")):
            player.heal(2)
    
    if(player.check_for_relic("Gluttonous Bag")):
            player.get_dice_pool().pop(random.randint(0, len(player.get_dice_pool()) - 1))
            player.add_gluttony()

    if(player.check_for_relic("Brimstone Crown")):
        player.take_damage(int(player.get_hellfire() // 10 * .75))
    else:
        player.take_damage(player.get_hellfire() // 10)

    if(player.check_for_relic("Glimmering Mirror")):
        random_dice = random.choice(player.get_dice_pool())
        player.get_dice_pool().append(Dice(random_dice.get_sides(), random_dice.get_type(), 1))

def game_loop(player, monster, game_manager):
    game = "on"
    while(game == "on" and player.get_health() > 0):
        print("Player Stats: ")
        print(player.get_overview())
        player.view_dice_pool()
        print()

        print(f"Dungeon: {game_manager.get_dungeon()}, Floor: {game_manager.get_floor()}")
        if(game_manager.get_floor() <= 2):
            monster.advanced_monster("Goblin", int((300 + 100 * (game_manager.get_dungeon() - 1)) * (game_manager.get_round_mod() * (game_manager.get_dungeon()))), int(10 * game_manager.get_round_mod()), 3)
        else:
            monster.advanced_monster("Troll", int((600 + 100 * (game_manager.get_dungeon() - 1)) * (game_manager.get_round_mod() * (game_manager.get_dungeon()))), int(15 * game_manager.get_round_mod()), 5)

        while(player.get_health() > 0 and monster.get_health() > 0):
            rolling_loop(player, monster)
            damage_loop(player, monster)
        end_of_combat_effects(player)
            
        if(player.get_health() <= 0):
            print("You Died!")
            game = "off"
            break


        print("Player Stats: ")
        print(player.get_overview())
        player.view_dice_pool()
        
        player.calculate_interest()
        shop_loop(player)
        game_manager.go_up_floor()

        save_answer = input("Would you like to save and quit? Y/N ")
        if(save_answer.upper() == "Y"):
            save_file = "4"
            while(save_file != "1" and save_file != "2" and save_file != "3"):
                save_file = input("Which save slot would you want to save in: 1 / 2 / 3? ")
                if(save_file == "1"):
                    save_game(game_manager, "save_file_one.json")
                elif(save_file == "2"):
                    save_game(game_manager, "save_file_two.json")
                elif(save_file == "3"):
                    save_game(game_manager, "save_file_three.json")
                else:
                    print("Incorrect Input. Please try again: ")
            break
            
def shop_loop(player):
    print()
    continue_shopping = "Y"
    chosen_dice = random.choices(DICE_POOL, weights=DICE_WEIGHTS, k=2)
    dice_stock = [deepcopy(d) for d in chosen_dice]
    shell_stock = random.choices(["Ruby", "Gold", "Ivory", "Iron", "Ethereal", "Vampiric", "Poisonous", "Radiant", "Infernal"], weights=[15, 15, 15, 15, 15, 15, 15, 4, 4], k=3)
    mask_stock = random.choices(SHOP_POOL, weights=MASK_WEIGHTS, k=2)
    relic_stock = random.choices(RELIC_POOL, weights=RELIC_WEIGHTS, k=2)
    while(continue_shopping.upper() == "Y"):
        print("1. Dice Shop")
        print("2. Relic Shop")
        print("3. Mask Shop")
        print("4. Shell Shop")
        choice = input("What would you like to do? ")
        if(choice == "1" or choice.lower() == "dice shop"):
            print(f"Gold: {player.get_money()} || Dice Stock: ")
            for dice in dice_stock:
                print(dice.get_dice_info())
            purchase = (input("Enter the # of the dice you want to buy, 0 to refresh (costs 1 gold), or any other # to leave. "))
            if(purchase.isdigit()):
                purchase = int(purchase)
                if(purchase <= len(dice_stock) and purchase > 0):
                    if(player.get_money() >= dice_stock[purchase - 1].get_price()):
                        player.spend_money(dice_stock[purchase - 1].get_price())
                        if(dice_stock[purchase - 1].get_type().upper() == "SHADOW"):
                            player.add_shadow(dice_stock[purchase - 1])
                        else:
                            player.add_to_dice_pool(dice_stock[purchase - 1])
                        dice_stock.pop(purchase - 1)
                    else:
                        print("You don't have enough Gold!")
                elif(purchase == 0):
                    if(player.get_money() >= 1):
                        chosen_dice = random.choices(DICE_POOL, weights=DICE_WEIGHTS, k=2)
                        dice_stock = [deepcopy(d) for d in chosen_dice]
                        player.spend_money(1)
                    else:
                        print("You don't have enough Gold!")
                else:
                    pass
        elif(choice == "2" or choice.lower() == "relic shop"):
            print(f"Gold: {player.get_money()} || Relic Stock: ")
            counter = 1
            for relic in relic_stock:
                print(f"{counter}. {relic['name']}, Desc: {relic['desc']} Price: {relic['price']}")
                counter += 1
            purchase = (input("Enter the # of the relic you want to buy, or any other # to leave. "))
            if(purchase.isdigit()):
                purchase = int(purchase)
                if(purchase <= len(relic_stock) and purchase > 0):
                    relic_choice = relic_stock[purchase - 1]
                    if(player.get_money() >= relic_choice['price']):
                        if(len(player.get_relic_list()) < 5):
                            player.spend_money(relic_choice['price'])
                            relic_stock.pop(purchase - 1)
                            player.add_relic(relic_choice['name'])
                            print(player.get_relic_list())
                        else:
                            print("You already have 5 relics.")
        elif(choice == "3" or choice.lower() == "mask shop"):
            print(f"Gold: {player.get_money()} || Mask Stock: ")
            counter = 1
            for mask in mask_stock:
                print(f"{counter}. {mask['name']}, Price: {mask['price']}, Sides: {mask['sides']}")
                counter += 1
            purchase = (input("Enter the # of the mask you want to buy, or any other # to leave. "))
            if(purchase.isdigit()):
                purchase = int(purchase)
                if(purchase <= len(mask_stock) and purchase > 0):
                    mask_choice = mask_stock[purchase - 1]
                    if(player.get_money() >= mask_choice['price']):
                        player.spend_money(mask_choice['price'])
                        mask_stock.pop(purchase - 1)
                        player.view_dice_pool()
                        dice_to_change = (input("Enter the # of the dice you want to re-mask. "))
                        if(dice_to_change.isdigit()):
                            dice_to_change = int(dice_to_change)
                            if(dice_to_change <= len(player.get_dice_pool()) and  dice_to_change > 0):
                                player.get_dice_pool()[dice_to_change - 1].change_sides(mask_choice['sides'])
                    else:
                        print("You don't have enough Gold!")
        elif(choice == "4" or choice.lower() == "shell shop"):
            counter = 1
            print(f"Gold: {player.get_money()} || Shell Stock: ")
            for shell in shell_stock:
                print(f"{counter}. {shell}, Price: 2")
                counter += 1
            purchase = (input("Enter the # of the shell you want to buy, or any other # to leave. "))
            if(purchase.isdigit()):
                purchase = int(purchase)
                if(purchase <= len(shell_stock) and purchase > 0):
                    if(player.get_money() >= 2):
                        player.spend_money(2)
                        shell_choice = shell_stock[purchase - 1]
                        shell_stock.pop(purchase - 1)
                        player.view_dice_pool()
                        dice_to_change = (input("Enter the # of the dice you want to re-mask. "))
                        if(dice_to_change.isdigit()):
                            dice_to_change = int(dice_to_change)
                            if(dice_to_change <= len(player.get_dice_pool()) and  dice_to_change > 0):
                                player.get_dice_pool()[dice_to_change - 1].change_type(shell_choice)
                    else:
                        print("You don't have enough Gold!")
        else:
            print("Incorrect Input, please try again!")
            print()
        continue_shopping = input("Would you like to continue shopping? Y/N: ")

def rolling_loop(player, monster):
    player.get_current_list_from_pool()
    if(player.check_for_relic("Echo Tome")):
        player.get_current_list().append(random.choice(player.get_current_list()))
        player.get_current_list().append(random.choice(player.get_current_list()))
    start_of_combat_effects(player)
    player.roll_current_list()

    print(f"Monster: {monster.get_name()}, HP: {monster.get_health()}, DMG: {monster.deal_damage()}, Poison Count: {monster.get_poisoned()}")

    print(f"{player.get_roll_info()} : {calculate_score(player)}")
    rolls = player.get_max_rolls()

    reroll_choice = input("Would you like to reroll any dice? Y/N: ")
    while(reroll_choice.upper() == "Y" and rolls >= 1):
        rolls -= 1
        reroll_indexes = input("Enter the # of the dice you want to reroll, seperated by a space: ")
        reroll_list = reroll_indexes.split(" ")
        player.reroll_dice(reroll_list)
        print(f"{player.get_roll_info()} : {calculate_score(player)}")
        if(rolls != 0):
            reroll_choice = input("Would you like to reroll any dice? Y/N: ")

def damage_loop(player, monster):
    check_for_after_round_dice(player, monster)
    poison_buff = 0
    for dice in player.get_dice_pool():
        if dice.get_type() == "Poisonous" and player.check_for_relic("Emerald Mask"):
            poison_buff += 1

    for i in range(0, monster.get_poisoned()):
        if(player.check_for_relic("Sulphuric Eye")):
            monster.take_dmg(monster.get_health() // 15 + poison_buff)
        else:
            monster.take_dmg(monster.get_health() // 10 + poison_buff)

    monster.take_dmg(calculate_score(player))

    if(player.get_health() > 0 and monster.health > 0):
        player.take_damage(monster.deal_damage())
        print(f"Player HP: {player.get_health()}\n")
    if(monster.health <= 0):
        player.add_money(monster.get_value())

def save_game(game_manager, filename):
    save_data = game_manager.save_data()
    with open(filename, "w") as file:
        json.dump(save_data, file, indent=4)
    
    print("success")

def wipe_data(filename):
    data = {
        'health': 100,
        'gold': 5,
        'dicePool': [{"sides": [1, 2, 3, 4, 5, 6], "type": "Basic", "price": 2}, {"sides": [1, 2, 3, 4, 5, 6], "type": "Basic", "price": 2}, {"sides": [1, 2, 3, 4, 5, 6], "type": "Basic", "price": 2}, {"sides": [1, 2, 3, 4, 5, 6], "type": "Basic", "price": 2}, {"sides": [1, 2, 3, 4, 5, 6], "type": "Basic", "price": 2}],
        'shadowPool': [],
        'hellfire': 0,
        'relicPool': [],
        'dungeon': 1,
        'floor': 1,
        'round_mod': 1
    } 

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Successfully Wiped Data For: {file.name}")

def load_game(game_manager, filename):
    with open(filename, "r") as file:
        load_data = json.load(file)

        loaded_dice_pool = []
        for dice in load_data["dicePool"]:
            loaded_dice_pool.append(Dice(dice["sides"], dice["type"], dice["price"]))

        loaded_shadow_pool = []
        for dice in load_data["shadowPool"]:
            loaded_shadow_pool.append(Dice(dice["sides"], dice["type"], dice["price"]))


    game_manager.load_data(load_data, loaded_dice_pool, loaded_shadow_pool)

def check_for_after_round_dice(player, monster):
    for dice in player.get_current_list():
        if dice.get_type() == "Vampiric":
            if(player.check_for_relic("Sharp Fangs")):
                if(player.check_for_relic("Batleather Cloak")):
                    player.take_damage(dice.get_result() * 2) - 2
                else:
                    player.take_damage(dice.get_result() * 2)
            else:
                if(player.check_for_relic("Batleather Cloak")):
                    player.take_damage(dice.get_result()) - 2
                else:
                    player.take_damage(dice.get_result())
        
        if dice.get_type() == "Ruby":
            if(player.check_for_relic("Bleeding Eye")):
                player.heal(dice.get_result() + 5)
            else:
                player.heal(dice.get_result())
            
        if dice.get_type() == "Radiant" and player.check_for_relic("Glowing Halo"):
            player.heal(len(player.get_dice_pool()))
        
        if dice.get_type() == "Gold":
            if(player.check_for_relic("Golden Glove")):
                player.add_money(2 + 2)
            else:
                player.add_money(2)
        if dice.get_type() == "Poisonous":
            if(player.check_for_relic("Viper's Fang")):
                monster.poison(2)
            else:
                monster.poison(1)

def check_for_pair(player):
    counts = Counter(player.get_results())
    return any(count >= 2 for count in counts.values())

def check_for_three_of_a_kind(player):
    counts = Counter(player.get_results())
    return any(count >= 3 for count in counts.values())

def check_for_four_of_a_kind(player):
    counts = Counter(player.get_results())
    return any(count >= 4 for count in counts.values())

def check_for_five_of_a_kind(player):
    counts = Counter(player.get_results())
    return any(count >= 5 for count in counts.values())

def calculate_base_score(player):
    sum = 0
    for dice in player.get_current_list():
        if(dice.get_type() == "Iron"):
            if(player.check_for_relic("Steel Helm")):
                sum += 150
            else:
                sum += dice.get_result() + 50
        else:
            sum += dice.get_result()

    for dice in player.get_dice_pool():
        if(player.check_for_relic("Suffocating Mask") and dice.get_type() == "Iron"):
            sum += 25
    
    sum += player.get_hellfire()
    return sum

def calculate_mult_mod(player):
    sum = 0
    for dice in player.get_current_list():
        if(dice.get_type() == "Ivory"):
            if(player.check_for_relic("Alabaster Mask")):
                sum += 4
            else:
                sum += 2
        elif(dice.get_type() == "Splinter"):
            sum += 2
        elif(dice.get_type() == "Radiant"):
            if(player.check_for_relic("Holy Blade")):
                sum += (len(player.get_dice_pool()) * 2)
            else:
                sum += len(player.get_dice_pool())
        elif(dice.get_type() == "Shadow" and player.check_for_relic("Black Dagger")):
            sum += 2
    
    if(player.check_for_relic("Magmatic Greatsword")):
        sum += player.get_hellfire() // 10

    for dice in player.get_dice_pool():
        if(player.check_for_relic("Withering Bone") and dice.get_type() == "Ivory"):
            sum += 1

    return sum

def calculate_mult_mult(player):
    sum = 0
    for dice in player.get_current_list():
        if(dice.get_type() == "Vampiric"):
            if(player.check_for_relic("Sharp Fangs")):
                sum += 4
            else:
                sum += 2
        
    if player.check_for_relic("Bloody Blindfold"):
        sum += 2
    
    if sum == 0:
        return 1
    else:
        return sum
    
def calculate_score(player):
    base_score = calculate_base_score(player)
    mult_mod = calculate_mult_mod(player)
    mult_mult = calculate_mult_mult(player)
    if(check_for_five_of_a_kind(player)):
        #print("Five of A Kind!")
        if(player.check_for_relic("Crown of Shadows")):
            return (600 + base_score) * ((3 + mult_mod) * mult_mult)
        else:
            return (600 + base_score) * ((3 + mult_mod) * mult_mult)
    elif(check_for_four_of_a_kind(player)):
        #print("Four of A Kind!")
        if(player.check_for_relic("Furious Greataxe")):
            return (500 + base_score) * ((2 + mult_mod) * mult_mult)
        else:
            return (400 + base_score) * ((2 + mult_mod) * mult_mult)
    elif(check_for_three_of_a_kind(player)):
        #print("Three of A Kind!")
        if(player.check_for_relic("Jagged Trident")):
            return (400 + base_score) * ((2 + mult_mod) * mult_mult)
        else:
            return (300 + base_score) * ((2 + mult_mod) * mult_mult)
    elif(check_for_pair(player)):
        #print("Pair!")
        if(player.check_for_relic("Tuning Fork")):
            return (300 + base_score) * ((1 + mult_mod) * mult_mult)
        else:
            return (200 + base_score) * ((1 + mult_mod) * mult_mult)
    else:
        #print("Chance!")
        return (100 + base_score) * ((1 + mult_mod) * mult_mult)

def main():
    cont = "Y"
    player = Player()
    monster = Monster()
    game_manager = Game_Manager(player, monster)
    cont = input("Would you like to play? Y/N: ")
    while(cont.upper() == "Y"):
        print("High Rollers: ")
        load_save = input("Would you like to load a save? Y/N: ")

        if(load_save.upper() == "Y"):
            save_file = "4"
            while(save_file != "1" and save_file != "2" and save_file != "3"):
                save_file = input("Which file would you like to load? 1 / 2 / 3 ? ")
                if(save_file == "1"):
                    load_game(game_manager, "save_file_one.json")
                elif(save_file == "2"):
                    load_game(game_manager, "save_file_two.json")
                elif(save_file == "3"):
                    load_game(game_manager, "save_file_three.json")
                else:
                    print("Incorrect Input. Please try again.")

                #dev-options: 
                if(save_file.lower() == "wipe data"):
                    wipe_data("save_file_one.json")
                    wipe_data("save_file_two.json")
                    wipe_data("save_file_three.json")

        else:
            player = Player()
            monster = Monster()
            game_manager = Game_Manager(player, monster)
            print("\nChoose your character: \n1. The Traveler: Start with five basic Dice.\n2. The Knight: Start with three Iron Dice, and a Heavy Blade.\n3. The Shade: Start with 50 Health, three Shadow Dice, two Basic Dice, and a Smoke Veil relic.")
            print("4. The Cleric: Start with two Radiant Dice.\n5. The Cursed: Start with one Ruby Die, and 100 Hellfire.\n6. The Vampire: Start with 50 health, one Vampiric Die, two Basic Dice, and a Sharp Fangs relic.\n")
            character = input("Choose which character you want: 1/2/3/4/5/6: ")
            if(character == "1"):
                pass
            elif(character == "2"):
                player.advanced_player(100, 3, 5, [Dice([1, 2, 3, 4, 5, 6], "Iron", 2), Dice([1, 2, 3, 4, 5, 6], "Iron", 2), Dice([1, 2, 3, 4, 5, 6], "Iron", 2)], 0, 0, [], ["Heavy Blade"])
            elif(character == "3"):
                player.advanced_player(50, 3, 5, [Dice([1, 2, 3, 4, 5, 6], "Basic", 2), Dice([1, 2, 3, 4, 5, 6], "Basic", 2)], 0, 0, [Dice([1, 2, 3, 4, 5, 6], "Shadow", 2), Dice([1, 2, 3, 4, 5, 6], "Shadow", 2), Dice([1, 2, 3, 4, 5, 6], "Shadow", 2)], ["Smoke Veil"])
            elif(character == "4"):
                player.advanced_player(100, 3, 5, [Dice([1, 2, 3, 4, 5, 6], "Radiant", 2), Dice([1, 2, 3, 4, 5, 6], "Radiant", 2)], 0, 0, [], [])
            elif(character == "5"):
                player.advanced_player(100, 3, 5, [Dice([1, 2, 3, 4, 5, 6], "Ruby", 2)], 0, 100, [], [])
            elif(character == "6"):
                player.advanced_player(50, 3, 5, [Dice([1, 2, 3, 4, 5, 6], "Vampiric", 2), Dice([1, 2, 3, 4, 5, 6], "Basic", 2), Dice([1, 2, 3, 4, 5, 6], "Basic", 2)], 0, 0, [], ["Sharp Fangs"])


        game_loop(player, monster, game_manager)
        cont = input("Would you like to play again? Y/N: ")




if __name__ == "__main__":
    main()