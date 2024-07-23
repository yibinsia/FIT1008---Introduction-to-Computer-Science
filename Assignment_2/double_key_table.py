from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Tuple, Any
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None: 
        """
        Best = Worst Case Complexity = O(1)
        """     
        if sizes is not None: 
            self.TABLE_SIZES = sizes    
        else:
            self.TABLE_SIZES = DoubleKeyTable.TABLE_SIZES 

        if internal_sizes is not None: 
            self.internal_sizes = internal_sizes 
        else:
            self.internal_sizes = self.TABLE_SIZES 
        self.index = 0 
        self.count = 0 
        self.array = ArrayR(self.TABLE_SIZES[self.index]) 

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """ 
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        Best case complexity: O(hash(key)) when key can be found at hashed position, the loop will break early.
        worst case complexity: O(n), where n is the length of table, when the table is heavy loaded and probing is often needed.
        """
        if self.count == self.table_size: 
            raise FullError('Table if full') 
        position1 = self.hash1(key1) 
        for _ in range(len(self.array)):  # O(len(self.array))
            if self.array[position1] is None: 
                if is_insert: 
                    table = LinearProbeTable(self.internal_sizes) 
                    table.hash = lambda k: self.hash2(k, table) 
                    self.array[position1] = (key1, table) 
                else:
                    raise KeyError(key1) 
            elif self.array[position1][0] == key1:  # O(key1comp==)
                break
            else:
                position1 = (position1 + 1) % self.TABLE_SIZES[0] 

        position2 = self.array[position1][1]._linear_probe(key2, is_insert)
        return position1, position2 

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        Best case complexity = worst case complexity = O(n) or O(m), n as the length of self.array, 
        m as the length of inner array, if key is none, it will iterates through 
        the top table and yields all keys in it. If key is not none, it will iterates
        through the inner array and yields all keys in it.
        """
        if key is None: 
            for i in range(len(self.array)):  #O(n)
                if self.array[i] is not None:
                    yield self.array[i][0]
        else:
            position1 = self.hash1(key) 
            current = 0        
            if self.array[position1][0] == key: 
                current = self.array[position1][1]                
            position1 += 1 
            for i in range(len(current.array)): #O(m)
                if current.array[i] is not None:
                    yield current.array[i][0] 
                    
    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        Best case complexity: O(n), n as the slots occupied of self.array, if key is None, the complexity is determine 
                                by the slots occupied of self.array.
        Worst case complexity: O(n*m), n as the slots occupied of self.array, m as the slots occupied of inner array, 
                                when key is not None, and both level table is heavy loaded, it can leads to O(n*m) complexity
                                to iterates through both table and get all keys.
        """
        outer_lst = [] 
        if key is None: 
            for i in range(len(self.array)): # O(n)
                if self.array[i] is not None: 
                    outer_lst.append(self.array[i][0])
            return outer_lst 
        else:
            for i in range(self.table_size): # O(n)
                if self.array[i] is not None: 
                    if self.array[i][0] == key: 
                        return self.array[i][1].keys() #O(m)
            raise KeyError

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        Best case complexity: O(m), m as the slots occupied in inner array, if key is not none, it will iterates through
                                the inner table and yields all values in it.
        Worst case complexity: O(n*m), n as the slots occupied in self.array, m as the slots occupied in inner array, 
                                if key is none, it yields all values in both table.
        """
        if key is None: 
            for i in range(len(self.array)): 
                if self.array[i] is not None: 
                    current = self.array[i][1] 
                    for j in range(self.array[i][1].table_size): 
                        if current.array[j] is not None:
                            yield current.array[j][1] 
        else:
            position1 = self.hash1(key) 
            current = 0 
            if self.array[position1][0] == key: 
                current = self.array[position1][1]           
            position1 += 1 
            for i in range(len(current.array)): 
                yield current.array[i][1] 

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        Best case complexity = Worst case complexity = O(n*m), n as the slots occupied in self.array, 
        m as the slots occupied in inner array, if key is none, the function iterates through the top-level array, 
        accesses the inner hash tables, and collects all values append to res. 
        If key is not none, iterates through the top-level array, checks if the current slot contains the desired key. 
        If the key is found, it accesses the inner hash table associated with it and collects its values.
        """
        res = [] 
        if key is None: 
            for i in range(len(self.array)): # O(n)
                if self.array[i] is not None: 
                    res += self.array[i][1].values() # O(m)
            return res

        elif key is not None:
            for i in range(len(self.array)): # O(n)
                if self.array[i] is not None: 
                    if self.array[i][0] == key: 
                        return self.array[i][1].values() # O(m)
            raise KeyError 

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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
        
    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        :complexity: See linear probe.
        """
        key1, key2 = key # O(1)
        position1,position2 = self._linear_probe(key1, key2, False) # O(Linear probe)
        return self.array[position1][1].array[position2][1] # O(1)
    
    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Best case complexity: O(hash(key)), when the key can be directly insert.
        Worst case complexity: O(n + _rehash), where n is the length of table, when the keys need to probe many times to find,
                               and the table is half full after setting item and need to rehash.
        """
        key1, key2 = key 
        position1, position2 = self._linear_probe(key1, key2, True)
        if self.array[position1][1].array[position2] is None: 
            self.count += 1 
        self.array[position1][1][key2] = data 
        if len(self.keys()) > self.table_size/2: 
            self._rehash() 

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        Best case complexity: O(hash(key)), when the key can be directly delete.
        Worst case complexity: O(n^2), where n is the length of table,when the keys need to probe
                                many times to find, and deleting item is midway through large chain.
        """  
        key1, key2 = key 
        position1, position2 = self._linear_probe(key1, key2, False) 
        if self.array[position1] is None: 
            raise KeyError("Key doesn't exist") 

        elif len(self.array[position1][1]) == 1: 
            self.array[position1] = None 
            self.count -= 1          
            position1 = (position1 + 1) % self.table_size 
            # When there's no more element at the position in both external and internal array, 
            # reinsert all the elements, this process stops when it reaches an empty slot
            while self.array[position1] is not None: 
                temp_key1 = self.array[position1][0] 
                for i in range(len(self.array[position1][1].array)): 
                    if self.array[position1][1].array[i] is not None: 
                        temp_key2, value = self.array[position1][1].array[i] 
                        self[temp_key1, temp_key2] = value 
                # If not at the same position, set to None
                if self.hash1(temp_key1) != position1:
                    self.array[position1] = None 
                # Update the position
                position1 = (position1 + 1) % self.table_size 
        else:
            del self.array[position1][1][key2] # Calls the internal table's _delitem_() to remove the key2 in the internal table
    
    def tablesize(self) -> int:
        """
        Return the current size of the table (different from the length)
        Best = Worst = O(1)
        """
        return len(self.array)

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        current_array = self.array 
        self.index += 1 
        if self.index >= len(self.TABLE_SIZES): 
            return 
        self.array = ArrayR(self.TABLE_SIZES[self.index]) 
        for item in current_array: 
            if item is not None: 
                key, value = item 
                newpos = self.hash1(key) 
                while self.array[newpos] is not None:
                    newpos += 1 
                self.array[newpos] = (key, value) 

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array) 
    
    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()