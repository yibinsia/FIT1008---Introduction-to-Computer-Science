from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING
from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.referential_array import ArrayR
import math

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6
    OPTIMISE_SPECIAL_INDEX = -1

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team_mode = team_mode
        self.selection_mode = selection_mode
        self.regenerate_array = None

        # Depending on the team mode, use the appropriate data structure for the team.
        if self.team_mode == self.TeamMode.FRONT: 
            self.team = ArrayStack(MonsterTeam.TEAM_LIMIT)
            
        elif self.team_mode == self.TeamMode.BACK:
            self.team = CircularQueue(MonsterTeam.TEAM_LIMIT)

        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.sort_key = kwargs.get("sort_key", None)
            self.team = ArraySortedList(MonsterTeam.TEAM_LIMIT)

        # Depending on the selection mode, populate the team using different methods.
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
            team_size = self.__len__()
            self.regenerate_array = ArrayR(team_size)
            empty_space = MonsterTeam.TEAM_LIMIT - team_size
            length_iteration = self.team.array.__len__() - empty_space
        
            for i in range(length_iteration): # Populate the regenerate_array without exceeding the maximum team size
                self.regenerate_array.__setitem__(i, self.team.array.__getitem__(i))

        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()         
            team_size = self.__len__()
            self.regenerate_array = ArrayR(team_size)
            empty_space = MonsterTeam.TEAM_LIMIT - team_size
            length_iteration = self.team.array.__len__() - empty_space

            for i in range(length_iteration):
                self.regenerate_array.__setitem__(i, self.team.array.__getitem__(i))

        elif selection_mode == self.SelectionMode.PROVIDED:
            self.provided_monsters = kwargs.get("provided_monsters",None)
            if len(self.provided_monsters) > 6:
                raise ValueError("Exceeded team capacity limit")
            
            for monsters in self.provided_monsters:
                if monsters.can_be_spawned() == False:
                    raise ValueError(monsters.get_name() + " cannot be spawned")
                
            self.select_provided(self.provided_monsters)
        else:
            raise ValueError(f"Selection mode {selection_mode} is not supported.")
        
    def __len__(self) -> int:
        """
        Get the length of monster team
        The best-case and worst-case time complexity is same as O(1) in __len__, 
        because it is simply returning a value.
        """
        return len(self.team)
        
    def add_to_team(self, monster: MonsterBase):
        """
        Adding monster into team with different mode.
        The best case and worst case of TeamMode.Front is O(1).
        The best case and worst case of TeamMode.Back is O(1).
        TeamMode.Optimise best case occurs when it add to back because it just time complexity of binary search O(logn).
        The worst case of TeamMode.Optimise occurs when adding a monster and the team needs 
        to be totally rearranged based on sorting keys.In this case, the worst case time complexity is 
        O(n) + binary search O(logn) = O(n) overall, n representing the number of monster currently present in the team.
        """
        if self.team_mode == self.TeamMode.FRONT:
            self.team.push(monster)

        elif self.team_mode == self.TeamMode.BACK:
            self.team.append(monster)

        elif self.team_mode == self.TeamMode.OPTIMISE: # Sort the added monster differently by different sort key
            if self.sort_key == self.SortMode.HP:
                sort_value = monster.get_hp()

            elif self.sort_key == self.SortMode.ATTACK:
                sort_value = monster.get_attack()

            elif self.sort_key == self.SortMode.DEFENSE:
                sort_value = monster.get_defense()

            elif self.sort_key == self.SortMode.SPEED:
                sort_value = monster.get_speed()

            elif self.sort_key == self.SortMode.LEVEL:
                sort_value = monster.get_level()

            sort_value *= MonsterTeam.OPTIMISE_SPECIAL_INDEX # Sort with descending order
            list_item = ListItem(monster, sort_value)
            self.team.add(list_item)

    def retrieve_from_team(self) -> MonsterBase:
        """
        Get monster back to team with different mode.
        The best case and worst case of TeamMode.Front is O(1).
        The best case and worst case of TeamMode.Back is O(1).
        The best case of TeamMode.OPTIMISE occurs when without needing to reorganize or shift any monster position. 
        In this case, the time complexity is depends on binary search which is O(logn).
        The worst case occurs when retrieving a monster in TeamMode.OPTIMISE and the team needs 
        to be totally rearranged based on sorting keys to maintains the sorted order. 
        In this case, the time complexity is O(n), n representing the number of monster currently present in the team.
        """
        if self.team_mode == self.TeamMode.FRONT:
            monster = self.team.pop()
            return monster

        elif self.team_mode == self.TeamMode.BACK:          
            monster = self.team.serve()
            return monster

        elif self.team_mode == self.TeamMode.OPTIMISE:
            list_item = self.team.delete_at_index(0)
            return list_item.value

    def special(self) -> None:
        """
        To swap monsters position or order in a team according to different TeamMode.

        The best case and worst case of special of TeamMode.Front is equals to O(1) because the for loops
        won't be affect by input.
        
        The best case of special of TeamMode.Back is when there is only 1 monster in the team,
        which no where to swap, in this case the time complexity will be O(1).
        The worst case of special of TeamMode.Back is similar with TeamMode.Front, the overall time 
        complexity will be O(n), n representing the length of team.

        The best case complexity of special of TeamMode.OPTIMISE is O(1), when there's only 1 monster in team.
        The worst case of special of TeamMode.OPTIMISE occurs when it has to resize, the for loop depends on n, 
        where n representing number of monster in the team, the .add function worst case will also be O(n)
        thus the overall worst case complexity will be O(n^2).
        """
        team_length = len(self.team)
        if self.team_mode == self.TeamMode.FRONT:
            temp_team = ArrayStack(MonsterTeam.TEAM_LIMIT)
            reversed_temp_team = ArrayStack(MonsterTeam.TEAM_LIMIT)
            if team_length >= 3: # If more than 3 monster in team, the first 3 at the front will be reversed
                for _ in range(3):
                    temp_team.push(self.team.pop())

                for _ in range(3):
                    reversed_temp_team.push(temp_team.pop())

                for _ in range(3):
                    self.team.push(reversed_temp_team.pop())

            elif team_length == 2: # If there is only 2 monster in team, they swapped position with each others
                                   # 1 monster in team is not be considered because it has no where to swap
                for _ in range(2):
                    temp_team.push(self.team.pop())

                for _ in range(2):
                    reversed_temp_team.push(temp_team.pop())

                for _ in range(2):
                    self.team.push(reversed_temp_team.pop())

        if self.team_mode == self.TeamMode.BACK:
            temp1 = CircularQueue(MonsterTeam.TEAM_LIMIT)
            temp2 = ArrayStack(MonsterTeam.TEAM_LIMIT) # A reversed order of original team
            temp3 = CircularQueue(MonsterTeam.TEAM_LIMIT) # A copy of original team
            if team_length >= 2:
                for _ in range(team_length):
                    temp1.append(self.team.serve())
                
                for _ in range(team_length):
                    i = temp1.serve()
                    temp2.push(i)
                    temp3.append(i)

                for _ in range(math.ceil(team_length / 2)): # Float division used for ceil up when the team length is odd
                    self.team.append(temp2.pop()) # Appending the swapped second half

                for _ in range(team_length // 2):
                    self.team.append(temp3.serve()) # Appending the original first half

        if self.team_mode == self.TeamMode.OPTIMISE:
            MonsterTeam.OPTIMISE_SPECIAL_INDEX *= -1 # Change the sort way from descending order to ascending or vice-versa
            temp_team_optimise = ArraySortedList(MonsterTeam.TEAM_LIMIT)
            for i in range(team_length):
                list_item = self.team.__getitem__(i)
                list_item_key = list_item.key * -1 # Invert the sorting key to reverse the order
                list_item_value = list_item.value
                temp_list_item = ListItem(list_item_value, list_item_key)
                temp_team_optimise.add(temp_list_item)
            self.team = temp_team_optimise

    def regenerate_team(self) -> None:
        """
        Revert the team to how it was on initialisation based on different selection mode.        
        When this function is executed, no matter what the selection mode is, the team will always be emptied and regenerated 
        according to the initial pattern, so the execution of the for loop is inevitable. Since it iterates through all monsters in the 
        regenerate_array or provided_monsters, this will resulting O(n) time complexity, which n representing the number of monster in 
        the regenerate array.
        The best case occurs when the add_to_team function is O(logn), then the overall complexity will be O(n * logn) = O(nlogn).
        The worst case occurs when add_to_team function is O(n), then the overall complexity will be O(n * n) = O(n^2).
        """
        if self.selection_mode == self.SelectionMode.RANDOM or self.selection_mode == self.SelectionMode.MANUAL:
            self.team.clear()
            for monsters in self.regenerate_array: # Get the array that saved original team in __init__
                self.add_to_team(monsters)

        if self.selection_mode == self.SelectionMode.PROVIDED:
            MonsterTeam.OPTIMISE_SPECIAL_INDEX = -1 # Make sure it sort with descending order after regenerated         
            self.team.clear()
            for monsters in self.provided_monsters:
                monsters_instance = monsters()
                self.add_to_team(monsters_instance)

    def select_randomly(self):
        """Generates monster into team randomly"""
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        
        Assume the input comes in O(1) time and is valid.
        The time complexity is depends on O(team_size), which is O(1) in the best case since the team size is bounded 
        between 1 and 6 for now, the while loop will loops maximum 6 times, consider add_to_team is best case, not using 
        TeamMode.Optimise, which is O(1), overall best case complexity will be O(1 * 1) = O(1).
        The worst-case occurs if the constant TEAM_LIMIT is not limit to 6,the while loop will loops m times which 
        m representing team size, considering add_to_team also having worst case complexity, worst case of TeamMode.Optimise
        O(n) in this case, n representing number of monster in the team, thus overall worst-case complexity will be O(m * n) = O(mn).
        """
        team_size = 0
        while True:
            try:
                team_size = int(input("How many monsters are there? "))
                if 1 <= team_size <= self.TEAM_LIMIT:
                    break
                else:
                    print("Please enter a valid integer between 1 and 6.") # Assume the TEAM_LIMIT is 6 in this case
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        monster_list = get_all_monsters()
        empty_space = team_size
        
        while empty_space > 0:
            print("Monster Are:")
            for i, monster in enumerate(monster_list):# Provide user monster list for selection 
                print(f"{i+1}: {monster_list[i].get_name()} [{'✔️' if monster.can_be_spawned() else '❌'}]")

            monster_selection = int(input("Which monster are you spawning?"))
            if 0 < monster_selection < len(monster_list) and monster_list[monster_selection - 1].can_be_spawned(): # -1 because the first monster start from index 0
                monster = get_all_monsters()[monster_selection - 1]
                self.add_to_team(monster())
                empty_space -= 1
            else:
                print("Invalid monster, Please try again")

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]

        Assume the provided team list is valid.
        The best-case time complexity of the function is proportional to the number of monster in the 
        provided_monsters list, which denoted as n, consider add_to_team is best case, O(1) in this case. 
        So, the overall best-case time complexity is O(n * 1) = O(n).
        The worst-case time complexity is also proportional to the number of monster in the 
        provided_monsters list, but consider add_to_team is worst case, O(n), which n representing number 
        of monster, in this case the overall worst-case time complexity is O(n * n) = O(n^2). 
        """
        if provided_monsters is not None:
            for monsters in provided_monsters:
                monsters_instance = monsters()# Get the monster's class
                self.add_to_team(monsters_instance)
        else:
            raise Exception("Team list provided is none")

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
