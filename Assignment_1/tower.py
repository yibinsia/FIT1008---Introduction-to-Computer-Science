from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue
class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.so_far = BSet()
        self.upcoming = BSet()

    def set_my_team(self, team: MonsterTeam) -> None:
        """
        Sets the player team and lives for the battle tower.
        The best-case time complexity equals to worst-case time complexity which both equals to O(1) in this function.
        Because its just simply assigning values.
        """
        self.my_team = team
        self.my_team.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_teams(self, n: int) -> None:
        """
        Randomly generates the enemy teams, and set up lives for each enemy team.
        The time complexity of the function is proportional to the integer n, which representing the number of tower teams 
        going to be generated. In this case the best-case time complexity equals to worst-case time complexity which both 
        equals to O(n).
        """
        self.tower_teams = CircularQueue(n)
        for _ in range(n):
            tower_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            tower_team.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES) 
            self.tower_teams.append(tower_team)
  
    def battles_remaining(self) -> bool:
        """
        Determine whether self team or enemy teams run out of lives or not.
        The best-case time complexity equals to worst-case time complexity which both equals to O(1) in this function.
        The comparison of integer is always O(1) and the is_empty function is also O(1) due to its implementation.
        """
        return self.my_team.lives > 0 and not self.tower_teams.is_empty()
            
    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """
        Simulates one battle in the tower, between the player team and the next enemy team. 
        The overall time complexity of the next_battle function is primarily determined by the loop over self.tower_teams, 
        resulting in O(n) complexity in the worst case, where n is the number of tower teams. 
        The best-case time complexity would be O(1) if there's only one tower team, as the loop would execute only once.
        """
        if self.my_team.lives > 0:
            self.my_team.regenerate_team()# Make sure the fainted monsters in the enemy team be regenerated, if the player team haven't run out of lives.
        for _ in range(len(self.tower_teams)):
            tower_team = self.tower_teams.serve()
            if tower_team.lives > 0:# Make sure the fainted monsters in the enemy team be regenerated, if the enemy team haven't run out of lives.
                tower_team.regenerate_team()  
                self.tower_teams.append(tower_team)

        enemy_team = self.tower_teams.serve()
        battle_result = self.battle.battle(self.my_team, enemy_team)
        # Modify lives value by battle result
        if battle_result == Battle.Result.TEAM1:
            enemy_team.lives -= 1
        elif battle_result == Battle.Result.TEAM2:
            self.my_team.lives -= 1
        elif battle_result == Battle.Result.DRAW:
            self.my_team.lives -= 1
            enemy_team.lives -= 1
        if enemy_team.lives > 0:
            self.tower_teams.append(enemy_team)
        return (battle_result, self.my_team, enemy_team, self.my_team.lives, enemy_team.lives)
    
    def out_of_meta(self) -> ArrayR[Element]:
        """
        Returning those elements met so far but not in the upcoming team.
        In the best case, the operations inside the loops for both enemy and self teams have constant time complexity.
        Similarly, the operation for calculating contains and creating the return_array involves iterating through the 
        Element enumeration, but the size of the Element enumeration is a fixed constant. Therefore, the best-case time complexity 
        is dominated by the constant time operations and the iteration through a constant-sized enumeration, so the 
        overall best-case time complexity will be O(1).
        The worst case occurs when you have to iterate through the entire self.tower_teams and the entire self.my_team to retrieve elements 
        for calculate "contains". Overall, the worst-case time complexity is proportional to the number of monsters in both enemy and self teams, 
        which is n. Therefore, the worst-case time complexity is O(n).
        """
        self.so_far = self.so_far.union(self.upcoming)#Save every elements that met before in so_far.
        self.upcoming.clear()    
        temp_queue = CircularQueue(len(self.tower_teams))
        enemy_team = self.tower_teams.serve()
        enemy_team.regenerate_team()#Make sure not missing to get every monster's element in the original enemy team.
        for i in range(len(enemy_team)):#Getting the element value of each monster in enemy team.
            monster = enemy_team.retrieve_from_team()
            element_name = Element.from_string(monster.get_element())
            element_value = element_name.value
            self.upcoming.add(element_value)   
  
        temp_queue.append(enemy_team) 
        for _ in range(len(self.tower_teams)):
            temp_queue.append(self.tower_teams.serve())
        self.tower_teams = temp_queue #To make sure self.tower_teams remains unchanged after served above
        self.my_team.regenerate_team()#Make sure not missing to get every monster's element in the original self team.
        for i in range(len(self.my_team)):#Getting the element value of each monster in self team.
            monster = self.my_team.retrieve_from_team()
            element_name = Element.from_string(monster.get_element())
            element_value = element_name.value 
            self.upcoming.add(element_value)

        contains = self.so_far.difference(self.upcoming)#Getting the element's value that should contain in out of meta 
        return_array = ArrayR(len(contains))
        i = 0
        for element in Element:#To turn the element's value to element's name and return the array for presentation
            if element.value in contains:
                return_array[i] = element
                i += 1
        return return_array

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)









