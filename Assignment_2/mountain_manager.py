from __future__ import annotations
from algorithms.mergesort import mergesort
from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        """
        Initializes the MountainManager with an empty list of mountains.
        
        Best and Worst Case Complexity: O(1)
        """
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adds a mountain to the manager.

        Best and Worst Case Complexity: O(1)
        """
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Removes a mountain from the manager.

        Best Case Complexity: O(1) if the mountain is at the start of the list
        Worst Case Complexity: O(N) if the mountain is at the end or not in the list, 
                                    where N is the total number of mountains in the manager
        """
        if mountain in self.mountains:
            self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Remove the old mountain and add the new mountain.

        Best Case Complexity: O(1) if the old mountain is at the start of the list
        Worst Case Complexity: O(N) if the old mountain is at the end or not in the list, 
                                    where N is the total number of mountains in the manager
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Returns a list of mountains with the specified difficulty level.

        Best and Worst Case Complexity: O(N) since we have to scan through all the mountains.
        """
        result = []
    
        for mountain in self.mountains:
            if mountain.difficulty_level == diff:
                result.append(mountain)
            
        return result

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Return a list of grouped mountains by their difficulty level in ascending order.

        Best and Worst Case Complexity: O(N log N) due to sorting of the mountains.
        """
        sorted_mountains = mergesort(self.mountains, key=lambda m: (m.difficulty_level, m.name))
        grouped_mountains = []
        current_group = []
        current_difficulty = None
    
        for mountain in sorted_mountains:
            if mountain.difficulty_level != current_difficulty:
                if current_group:
                    grouped_mountains.append(current_group)
                current_group = [mountain]
                current_difficulty = mountain.difficulty_level
            else:
                current_group.append(mountain)
    
        if current_group:
            grouped_mountains.append(current_group)
    
        return grouped_mountains