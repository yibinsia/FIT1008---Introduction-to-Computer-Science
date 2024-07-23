from __future__ import annotations
from enum import auto
from typing import Optional
from base_enum import BaseEnum
from team import MonsterTeam

class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity
        
    def process_turn(self) -> Optional[Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed. 
        The best case occurs when the action chosen is not SPECIAL, function choose_action time complexity is O(1), because it is 
        just comparison of integer, the time complexity of add_to_team and retrieve_from_team should be O(1) if considering best case, 
        the rest of the function or operation will all be O(1). Overall the best case time complexity will be O(1).
        The worst case occurs when the action chosen is SPECIAL, and consider add_to_team, retrive_from_team, and special all 
        are worst case, the worst case complexity will be O(n) + O(n) + O(n^2), overall the worst case complexity will be O(n^2).
        """
        team1_action = self.team1.choose_action(self.out1, self.out2)
        team2_action = self.team2.choose_action(self.out2, self.out1)
        
        if team1_action == self.Action.SWAP:
            self.team1.add_to_team(self.out1)
            self.out1 = self.team1.retrieve_from_team()
        
        elif team1_action == self.Action.SPECIAL:
            self.team1.add_to_team(self.out1)
            self.team1.special()
            self.out1 = self.team1.retrieve_from_team()

        if team2_action == self.Action.SWAP:
            self.team2.add_to_team(self.out2)
            self.out2 = self.team2.retrieve_from_team()

        elif team2_action == self.Action.SPECIAL:
            self.team2.add_to_team(self.out2)
            self.team2.special()
            self.out2 = self.team2.retrieve_from_team()

        if team1_action == self.Action.ATTACK and team2_action != self.Action.ATTACK:
            self.out1.attack(self.out2)
        
        elif team2_action == self.Action.ATTACK and team1_action != self.Action.ATTACK:
            self.out2.attack(self.out1)

        # Compare speed stat if both choose action attack simultaneously
        # Monster having greater speed attack first, if equals then attack each other simultaneously
        elif team1_action == self.Action.ATTACK and team2_action == self.Action.ATTACK:
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                if self.out2.alive():
                    self.out2.attack(self.out1)

            elif self.out2.get_speed() > self.out1.get_speed():
                self.out2.attack(self.out1)
                if self.out1.alive():
                    self.out1.attack(self.out2)
            
            else:
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)

        if self.out1.alive() and self.out2.alive():
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp() - 1)
         
        # Handle evolution for monster alive
        if self.out2.alive() and not self.out1.alive():
            self.out2.level_up()
            self.out2 = self.out2.evolve()
            if len(self.team1) > 0:
                self.out1 = self.team1.retrieve_from_team()
        
        elif self.out1.alive() and not self.out2.alive():
            self.out1.level_up()
            self.out1 = self.out1.evolve()
            if len(self.team2) > 0:
                self.out2 = self.team2.retrieve_from_team()
                  
        # Check for battle result
        if self.out1.alive() and not self.out2.alive():
            return self.Result.TEAM1
        elif self.out2.alive() and not self.out1.alive():
            return self.Result.TEAM2
        elif not self.out1.alive() and not self.out2.alive():
            return self.Result.DRAW
        else:
            return None
            
    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
