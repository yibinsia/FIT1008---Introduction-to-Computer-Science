from __future__ import annotations
import abc
from stats import Stats
from elements import EffectivenessCalculator
from elements import Element
import math
class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.simple_mode = simple_mode
        self.initial_level = level
        self.level = level
        self.current_hp = self.get_max_hp()

    def get_level(self):
        """The current level of this monster instance"""
        return self.level
    
    def level_up(self):
        """Increase the level of this monster instance by 1"""
        hp_lost = self.get_max_hp() - self.get_hp()
        self.level += 1
        self.set_hp(self.get_max_hp() - hp_lost)

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.current_hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.current_hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().get_attack()
        
        else:
            return self.get_complex_stats().get_attack(self.level)

    def get_defense(self):
        """Get the defense of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().get_defense()
        
        else:
            return self.get_complex_stats().get_defense(self.level)

    def get_speed(self):
        """Get the speed of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().get_speed()
        
        else:
            return self.get_complex_stats().get_speed(self.level)

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().get_max_hp()
        
        else:
            return self.get_complex_stats().get_max_hp(self.level)

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.get_hp() > 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance
        The best case and worst case time complexity of attack will both be O(1),
        because it is just performing operation and assigning values.
        """
        attack_stat = self.get_attack()
        defense_stat = other.get_defense()

        if defense_stat < attack_stat / 2: # Calculate damage based on some logics given in description.
            damage = attack_stat - defense_stat
        elif defense_stat < attack_stat:
            damage = attack_stat * 5 / 8 - defense_stat / 4
        else:
            damage = attack_stat / 4

        element_1 = Element.from_string(self.get_element()) # Calculating damage based on type's effectiveness
        element_2 = Element.from_string(other.get_element())
        multiplier = EffectivenessCalculator.get_effectiveness(element_1, element_2)
        effective_damage = math.ceil(damage * multiplier)
        other.set_hp(other.get_hp() - effective_damage)


    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        return self.get_evolution() is not None and self.get_level() > self.initial_level

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if self.ready_to_evolve():
            hp_lost = self.get_max_hp() - self.get_hp()
            evolution_class = self.get_evolution()
            new_instance =  evolution_class(self.simple_mode, self.level)
            new_instance.current_hp -= hp_lost
            return new_instance

        else:
            return self
        
    def __str__(self):
        """Return a string representation of the Monster instance."""
        return f"LV.{self.level} {self.get_name()}, {self.current_hp}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

