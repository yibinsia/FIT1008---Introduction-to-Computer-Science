from island import Island
from data_structures.bst import BinarySearchTree

class Mode1Navigator:
    """
    Approach:
    The `Mode1Navigator` class is designed to optimize the selection of islands for crew visits in the Davy Back Fight. The approach leverages 
    a Binary Search Tree (BST) to prioritize islands based on their marines-to-money ratio. This choice of data structure allows for the efficient 
    selection of islands that offer the lowest cost but the highest potential profit. The code implementation retrieves islands from the BST in 
    ascending order of their ratios, ensuring that the crew visits the most profitable islands first.

    Data Structures Used:
    Binary Search Tree (BST): The BST is employed to store the islands based on their marines-to-money ratio. This enables quick retrieval of islands 
    with the most favorable cost-to-profit ratio. The BST is unbalanced, resulting in a time complexity of O(N) when the crew is allocated to visit all islands.

    A Small Example:
    Consider a simplified example with four islands and a crew size of 100:
    - Island A: Money = 200, Marines = 100 (Ratio = 0.5)
    - Island B: Money = 300, Marines = 100 (Ratio = 0.33333)
    - Island C: Money = 500, Marines = 100 (Ratio = 0.2)
    - Island D: Money = 150, Marines = 100 (Ratio = 0.66667)

    The `Mode1Navigator` is initialized with these islands and a crew size of 100. The select_islands method areturns a list of selected islands along with the 
    number of crew to send to maximize profit. In this example, it might select the islands in the order C, B, A, D, based on their marines-to-money ratios.

    Complexity Reasoning:
    - Best Case:
        - The best-case scenario occurs when the crew size has been fully used up to visit the first island, resulting in a time complexity of O(1),
        refer to above example, after visit Island C, all the crew will be sent to first island and left no crew to send to other island, so the loop in selected_islands will
        break early.
    - Worst Case:
        - The worst-case scenario arises when the BST is unbalanced, and the crew has to visit all islands. In this case, the select_islands method has a time complexity of O(N), 
        where N is the number of islands.
    - Select Islands from Crew Numbers:
        - This method returns the list of money made by visiting islands with different crew sizes. The best-case complexity is O(C) when all crew has been used 
        up to visit the first island in each different crew size. The worst-case complexity is O(C * N), where C is the number of different crew sizes, and N is 
        the number of islands if all islands are visited with all crew sizes.
    - Update Island:
        - Updating an island's attributes has a constant time complexity of O(1), as it simply involves modifying the island's attributes.

    The use of a BST in the `Mode1Navigator` class allows for efficient island selection based on the marines-to-money ratio, prioritizing islands with the lowest 
    cost and highest profit, making it an effective strategy for the Davy Back Fight.
    """
    
    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Best = Worst = O(N), where N is the number of islands.
        """
        self.island_bst = BinarySearchTree() 
        self.crew = crew
        # Insert islands into the BST using their ratio as the key
        for island in islands: # O(N)
            ratio = island.marines / island.money
            self.island_bst[ratio] = island

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        This method will return the list of island selected along 
        with the number of crew you will be sending so
        that visiting those island, will make the most money.
        Best: O(1), if the crew has all been used up to visit the first island.
        Worst: O(N), where N is the number of islands, if the BST is unbalanced, 
                and the crew has to visit all islands.
        """
        selected_islands = []
        crew_remaining = self.crew 
        
        for island in self.island_bst: # O(N)
            if crew_remaining <= 0:
                break
            crew_to_send = min(crew_remaining, island.item.marines)
            selected_islands.append((island.item, crew_to_send))
            crew_remaining -= crew_to_send
        return selected_islands
        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        This method will return the list of money made by visiting the islands 
        with different crew numbers.
        Best: O(C), if all crew been used up to visit the first island, in all the different crew size.
        Worst: O(C*N), where C is the number of different crew size, N is the number of islands,
                 if the crew has to visit all islands, in all the different crew size.
        """
        results = []

        for crew_size in crew_numbers: # O(C)
            crew_remaining = crew_size
            total_money = 0
            if self.crew > 0:
                for island in self.island_bst: # O(N)
                    crew_to_send = min(crew_remaining, island.item.marines)
                    total_money += island.item.money * crew_to_send / island.item.marines 
                    crew_remaining -= crew_to_send
            results.append(total_money)   

        return results

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Best = Worst = O(1), simply update the island's attributes.
        """
        # Update the island's attributes
        island.money = new_money
        island.marines = new_marines


    