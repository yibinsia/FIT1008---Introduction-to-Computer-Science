from __future__ import annotations
from algorithms.mergesort import merge, mergesort
from algorithms.binary_search import binary_search
from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Initializes a new instance of the MountainOrganiser class.

        Attributes:
        sorted_mountains (List[Mountain]): A list of mountains sorted by difficulty and name.
        sorted_keys (List[Tuple]): A list of keys (difficulty, name) corresponding to sorted_mountains.

        Best and Worst Case Complexity: O(1)
        """
        self.sorted_mountains = []
        self.sorted_keys = []
    
    def cur_position(self, mountain: Mountain) -> int:
        """
        Retrieves the current position (rank) of a given mountain.
        Returns the position (rank) of the mountain.
        Raises KeyError if the mountain has not been added yet.

        Best and Worst Case Complexity: O(log N) where N is the total number of mountains included so far.
        """
        key = (mountain.difficulty_level, mountain.name)
        position = binary_search(self.sorted_keys, key)
        if position < len(self.sorted_keys) and self.sorted_keys[position] == key:
            return position
        else:
            raise KeyError(f"The mountain {mountain.name} hasn't been added yet.")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser.

        Best and Worst Case Complexity: O(M log(M) + N) where M is the number of mountains being added and 
                                                              N is the total number of mountains included so far.
        """
        # Create the sorted keys for the new mountains
        sorted_keys_new = []
        for m in mountains:
            key = (m.difficulty_level, m.name)
            sorted_keys_new.append(key)
        
        # Sort the new mountains list
        sorted_mountains_new = mergesort(mountains, key=lambda m: (m.difficulty_level, m.name))
        sorted_keys_new = mergesort(sorted_keys_new)
        
        # Merge the current sorted list and the new list of mountains (and their keys)
        merged_mountains = merge(self.sorted_mountains, sorted_mountains_new, key=lambda m: (m.difficulty_level, m.name))
        merged_keys = merge(self.sorted_keys, sorted_keys_new)
        
        self.sorted_mountains = merged_mountains
        self.sorted_keys = merged_keys