from island import Island
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    Approach:
    The `simulate_day` method is designed to simulate a day of the Davy Back Fight, where captains aim to choose islands that can yield the highest loot. 
    To achieve this, we utilize a MaxHeap data structure to efficiently select islands with the maximum potential profit. 
    The MaxHeap ensures that the island with the most money per marine remains at the top of the heap, making it the preferred choice for captains.

    Data Structures Used:
    MaxHeap: MaxHeap is used to store the islands with the sorting order of (money - 2*marines) modified in island.py. It allows for quick retrieval of the island with 
    the highest score, facilitating efficient decision-making by captains because this will satisfied the score calculation (2*C+M) states in specification,
    where C is the number of crew members and M is the amount of money. The `heapify` method is used to maintain the MaxHeap's integrity by reorganizing the islands 
    whenever their attributes change.

    A Small Example:
    Consider a simplified example with three islands and two captains:
    The score is based on my sorting algorithm, money - 2*marines, which will sort the same as the specification.
    - Island A: Money = 300, Marines = 50, Score = 200
    - Island B: Money = 200, Marines = 40, Score = 120
    - Island C: Money = 150, Marines = 30, Score = 90

    Two captains with a crew size of 50 each are participating. The `simulate_day` method aims to find the most profitable islands for the captains to plunder.

    At the start, the MaxHeap might look like this:
    MaxHeap: [(200, Island A), (120, Island B), (90, Island C)]

    In the first iteration, the first captain selects Island A, as it offers the highest score(pop by get_max). The MaxHeap is updated:
    MaxHeap: [(120, Island B), (90, Island C)]

    In the second iteration, the second captain selects Island B, as it offers the highest score after Island A has been fully plundered. The MaxHeap is updated once more:
    MaxHeap: [(90, Island C)]

    The method proceeds until all captains have made their selections.

    Complexity Reasoning:
    Best = Worst = O(N + C*log(N)), where C is the number of captains, N is the number of islands with non-zero money.
                    The heapify method has a sorting time complexity of O(N), where N is the number of islands. While there is C number of
                    captains, and for each captain, popping the maximum island from the heap. This operation (get_max) has a complexity of O(log N), 
                    and it iterates over each captain causes C times so the overall time complexity of the simulate_day method is O(N + C*log(N)).

    The MaxHeap data structure ensures that captains consistently make optimal choices by efficiently retrieving islands with the highest money per marine, 
    making this approach effective for the Davy Back Fight simulation.
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Best = Worst = O(1)
        """
        self.n_pirates = n_pirates
        self.islands = []  
        
    def add_islands(self, islands: list[Island]) -> None:
        """
        Add a list of islands to the seas.
        Best = Worst = O(N), where N is the number of islands.
        """
        self.islands.extend(islands)

    def simulate_day(self, crew: int) -> list[tuple[Island, int]]:
        """
        Simulate a day of the Davy Back Fight. Crew is the size of the crew for every pirate captain.
        Return a list of tuples representing the choices made by each pirate captain.
        Best = Worst = O(N + C*log(N)), where N is the number of islands with non-zero money, C is the number of captains, 
                        the heapify tooks O(N) time complexity to sort the islands,
                        the get_max() causes O(log(N)) time complexity and there is C number of captains. 
                        Overall causes O(N + C*log(N)) time complexity.
        """
        results = []
        money_heap = MaxHeap.heapify(self.islands) # O(N)
        for pirate in range(self.n_pirates): # O(C)
            if len(money_heap) == 0:
                results.append((None, 0))
            else:
                selected_island = money_heap.get_max() # O(log(N))
                crew_to_send = min(crew, selected_island.marines)
                money_looted = min(crew_to_send * selected_island.money / selected_island.marines, selected_island.money)
                results.append((selected_island, crew_to_send))
                selected_island.money -= money_looted
                selected_island.marines -= crew_to_send    
                if selected_island.money > 0:
                    money_heap.add(selected_island)      
        
        return results
        