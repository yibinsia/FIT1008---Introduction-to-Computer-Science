from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self):
        """
        Best = worst case complexity = O(1)
        """
        self.array = ArrayR(self.TABLE_SIZE)
        self.level = 0
        self.count = 0
        
    def hash(self, key):
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1
    
    def __getitem__(self, key):
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        Best case complexity = O(1), when the key is at the top table.
        Worst case complexity = O(n), where n is the depth of the table, when the key is at the bottom table
                                recursive calls until reached the bottom table leads to O(n) complexity.
        """
        position = self.hash(key) 
        # Base Case 1
        if self.array[position] is None: 
            raise KeyError ('Key does not exist') 
        # Base Case 2
        elif type(self.array[position][1]) != InfiniteHashTable:
            if self.array[position][0] == key:
                return self.array[position][1] 
            else:
                raise KeyError ('Key does not exist')
        # Recursive Call 
        elif type(self.array[position][1]) == InfiniteHashTable: 
            next_table = self.array[position][1] 
            return next_table[key] # Go to the next table and call next_table's _getitem_() to get the value of the given key

    def __setitem__(self, key, value):
        """
        Set an (key, value) pair in our hash table.
        Best case complexity: O(1), when the key is insert at the top table.
        Worst case complexity: O(n), where n is the depth of the table, when there is a long chain of child tables,
                                which means a lot of collisions occur, recursive calls until reached the bottom table 
                                and create a new infinitehashtable to insert key-value pair causes overall O(n) complexity.
        """      
        position = self.hash(key)
        current_table = self.array
        # Base Case 1
        if current_table[position] is None:        
            current_table[position] = (key, value)   
            self.count += 1
        else:      
            if type(current_table[position][1]) != InfiniteHashTable:  
                # Base Case 2                  
                if key == current_table[position][0]:# At the final table, if the key already exists, update the value                   
                    current_table[position] = (key, value)       
                else:
                    temp = current_table[position]
                    new_table = InfiniteHashTable()
                    new_table.level = self.level + 1           
                    current_table[position] = (current_table[position][0:new_table.level], new_table) # Replace the value with the new child InfiniteHashTable
                    new_table[temp[0]] = temp[1] 
                    new_table[key] = value 
                    self.count -= 1
            else:
                next_table = current_table[position][1]
                next_table[key] = value

    def __delitem__(self, key):
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        Best case complexity = O(1), when the key is at the top table, key can be deleted directly.
        Worst case complexity = O(n^3), where n is the depth of table, when the key is at the bottom table, 
                                recursive calls until reached the bottom table, and collapse all the way back to parent table
                                causes O(n^3) complexity.
        """
        position = self.hash(key) 

        # Base Case 1
        if self.array[position] is None: 
            raise KeyError ("Key does not exist") 

        # Base Case 2
        elif type(self.array[position][1]) != InfiniteHashTable and self.array[position][0] == key: 
            self.array[position] = None
            self.count -= 1
            if self.count == 1 and self.level != 0:
                # Get the last key-value pair in the table and set it to the parent_table
                for i in range(len(self.array)): 
                    if self.array[i] is not None: 
                        temp = self.array[i] 
                        self.array[i] = None
                        self.count -= 1 
                        self.collapse(temp[0], temp[1]) 
        # Recursive Call 
        else:
            next_table = self.array[position][1]
            del next_table[key] # Recursive Call (Go to the next table and call next_table's _setitem_() to set the (key,value) pair)

    def collapse(self, key, value):
        """
        A function that collapses the table when there is only one (key, value) pair left in the table.
        Best case complexity = O(n), where n is the depth of the table, when current table is parent table.
        worst case complexity = O(n^2), where n is the depth of the table, when it collapse all the way back to parent table.
        """
        position = self.hash(key) 
        # Base Case 1 (Reached the top table)
        if self.level == 0: 
            self.array[position] = (key, value) 
            self.count += 1 
        else:
            # Base Case 2 (if the table still have other (key, value) pair inside
            if self.count != 0: 
                self.array[position] = (key, value) 
                self.count += 1 
            else:
                # Recursive Call
                self.parent_table = self.find_parent_table(key)
                self.parent_table.collapse(key, value)

    def find_parent_table(self, key):
        """
        Find the parent table of the current table.
        Best case complexity = O(1), when current table is top table.
        Worst case complexity = O(n), where n is the total number of level of the current table, 
                                when current table is the deepest table, traverse back to find parent table
                                causes linear complexity.
        """
        position = self.hash(key)
        current_table = self.array
        if current_table[position][1].level == 1:
            self.parent_table = current_table
            return       
        elif current_table[position][1].level > 1:
            previous_table[position][1] = current_table
            return previous_table.find_parent_table()
    
    def __len__(self) -> int:
        # Loop through the entire array, if there is an InfiniteHashTable, calls its __len__() to get the number of (key, value) pair
        count = self.count        
        for i in range(len(self.array)): 
            if self.array[i] is not None and type(self.array[i][1]) == InfiniteHashTable:
                new_table = self.array[i][1]
                count += len(new_table) # Recursive Call (Go to the next table and call next_table's _len_() to get the number of (key, value) pair
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        Best case complexity = O(1), when the key is at the top table, which means the sequence contains only 1 element.
        Worst case complexity = O(n), where n is the depth of the table, when the key to be access is at the bottom table, 
                                which means the sequence contains n elements.
        """
        position = self.hash(key) 
        # Base Case 1
        if self.array[position] is None:
            raise KeyError ('Key does not exist')
        else: 
            if type(self.array[position][1]) != InfiniteHashTable: 
                if self.array[position][0] == key: 
                    return [position]  # Base Case 2
                else:
                    raise KeyError('Key does not exist') # Base Case 3
            else: 
                next_table = self.array[position][1] # O(1)
                return [position] + (next_table.get_location(key)) # recursively call the child table's get_location() and combine the result of the sub-problem
            
    
    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
        
    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        Best = worst case complexity = O(n), where n is the number of (key, value) pair in the table.
        """
        if current is None:
            current = self.array
        sorted_keys = []

        for entry in current:
            if entry is None:
                continue
            if type(entry[1]) != InfiniteHashTable:
                sorted_keys.append(entry[0])
            else:
                next_table = entry[1]
                sorted_keys.extend(next_table.sort_keys())
        return sorted(sorted_keys)






