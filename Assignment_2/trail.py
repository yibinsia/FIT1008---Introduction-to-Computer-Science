from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack
# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        
        return self.following.store
        

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
       
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        new_series = TrailSeries(mountain, Trail(self))
        return new_series

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        new_series = TrailSplit(top=Trail(), bottom=Trail(), following=Trail(self))
        return new_series

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        new_series = TrailSeries(self.mountain, Trail(TrailSeries(mountain, Trail(self))))
        return new_series

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        new_split = TrailSplit(top=Trail(), bottom=Trail(), following=self.following)
        new_series = TrailSeries(self.mountain, Trail(new_split))
        return new_series

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        if self.store is None:
            return Trail(TrailSeries(mountain=mountain, following=Trail()))
        else:
            return self.store.add_mountain_before(mountain)

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        if self.store is None:
            return Trail(TrailSplit(top=Trail(), bottom=Trail(), following=Trail()))
        else:
            return self.store.add_empty_branch_before()

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        Best: O(1), if the trail is empty.
        Worst: O(N), where N is the number of trails in the path.
        """
        from personality import PersonalityDecision
        stack = LinkedStack[Trail]()
        trailstack = LinkedStack[Trail]()
        trailstack.push(self)
        current_trail = trailstack.pop()
        current_store = current_trail.store
        
        while True:

            if current_store.__class__.__name__ == "TrailSplit":
                decision = personality.select_branch(current_store.top, current_store.bottom)
                
                if decision == PersonalityDecision.TOP:
                    stack.push(current_store.following)
                    current_store = current_store.top.store  # Update current trail to the top branch
                elif decision == PersonalityDecision.BOTTOM:
                    stack.push(current_store.following)
                    current_store = current_store.bottom.store  # Update current trail to the bottom branch
                elif decision == PersonalityDecision.STOP:
                    break
                
            elif current_store.__class__.__name__ == "TrailSeries":
                personality.add_mountain(current_store.mountain)
                current_store = current_store.following.store  # Update current trail to the following trail

            elif current_store is None and not stack.is_empty():
                following_trail = stack.pop()  # Get the previous trail from the stack
                if following_trail is not None:
                    current_store = following_trail.store  # Update current trail to the following trail
                     
            else:
                break

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        mountains = []
        stack = LinkedStack[Trail]()
        stack.push(self)

        while not stack.is_empty():
            current_trail = stack.pop()
            if current_trail.store:
                if current_trail.store.__class__.__name__ == "TrailSeries":
                    mountains.append(current_trail.store.mountain)
                    stack.push(current_trail.store.following)
                elif current_trail.store.__class__.__name__ == "TrailSplit":
                    stack.push(current_trail.store.top)
                    stack.push(current_trail.store.bottom)
                    stack.push(current_trail.store.following)
        return mountains
        
    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        paths = []
        stack = LinkedStack[Trail]()
        stack.push(self)

        while not stack.is_empty():
            current_trail = stack.pop()
            if current_trail.store:
                if current_trail.store.__class__.__name__ == "TrailSeries":
                    if current_trail.store.mountain.difficulty_level <= max_difficulty:
                        paths.append(current_trail.collect_all_mountains())
                    stack.push(current_trail.store.following)
                elif current_trail.store.__class__.__name__ == "TrailSplit":
                    stack.push(current_trail.store.top)
                    stack.push(current_trail.store.bottom)
                    stack.push(current_trail.store.following)
        return paths


    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
