# Name: Richelle Thompson
# OSU Email: thomrich@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/24
# Description: An implementation of a HashMap using open addressing with
#              quadratic probing. A dynamic array is used to store the hash
#              table, and each index of the array can contain at most one
#              element - a HashEntry object containing a key and value.
#              When removing an element, the object remains in the array,
#              but its data member is_tombstone is set to True.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the key already
        exists, the associated value is replaced with the new value.
        If the key is not in the hash map, a new key/value pair is added.
        """
        # Resize table to double its current capacity if load is too high
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        # Find initial index where an element containing the key could exist
        initial_index = self._find_initial_index(key)
        j = 0

        while True:
            # Quadratic probing index
            index = self._find_quad_index(initial_index, j)
            element = self._buckets[index]

            # Found an empty index, insert key/value pair here
            if element is None:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return

            # Found an element containing the key, update its associated value.
            # If it's a tombstone, make it not a tombstone anymore.
            elif element.key == key:
                if element.is_tombstone:
                    element.is_tombstone = False
                    self._size += 1
                element.value = value
                return

            # Didn't find an empty index or the key, continue probing
            j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. The capacity must be
        a prime number. All active key/value pairs are put in the new table
        (all non-tombstone elements are rehashed).
        """
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store all active key/value pairs, then resize and clear the map
        da = self.get_keys_and_values()
        self._capacity = new_capacity
        self.clear()

        # Put key/value pairs back into the map
        for index in range(da.length()):
            self.put(da[index][0], da[index][1])

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # Capacity = number of buckets, size = number of non-empty buckets
        return self.get_capacity() - self.get_size()

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not
        in the hash map, returns None.
        """
        # Find initial index where an element containing the key could exist
        initial_index = self._find_initial_index(key)
        j = 0

        while True:
            # Quadratic probing index
            index = self._find_quad_index(initial_index, j)
            element = self._buckets[index]

            # Found an empty index, key doesn't exist
            if element is None:
                return None

            # Found an element containing the key. If it's a tombstone,
            # the element doesn't exist in the map.
            elif element.key == key:
                if element.is_tombstone:
                    return None
                return element.value

            # Didn't find an empty index or the key, continue probing
            j += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns
        False.
        """
        # Find initial index where an element containing the key could exist
        initial_index = self._find_initial_index(key)
        j = 0

        while True:
            # Quadratic probing index
            index = self._find_quad_index(initial_index, j)
            element = self._buckets[index]

            # Found an empty index, key doesn't exist
            if element is None:
                return False

            # Found an element containing the key. If it's a tombstone,
            # the element doesn't actually exist in the map.
            elif element.key == key:
                if element.is_tombstone:
                    return False
                return True

            # Didn't find an empty index or the key, continue probing
            j += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        # Find initial index where an element containing the key could exist
        initial_index = self._find_initial_index(key)
        j = 0

        while True:
            # Quadratic probing index
            index = self._find_quad_index(initial_index, j)
            element = self._buckets[index]

            # Found an empty index, key doesn't exist
            if element is None:
                return

            # Found an element containing the key, remove it. If it's a
            # tombstone, it was already previously removed.
            elif element.key == key:
                if element.is_tombstone:
                    return
                element.is_tombstone = True
                self._size -= 1
                return

            # Didn't find an empty index or the key, continue probing
            j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map.
        """
        da = DynamicArray()

        # Check each index for a HashEntry object that isn't a tombstone
        for index in range(self._capacity):
            element = self._buckets[index]
            if element and not element.is_tombstone:
                da.append((element.key, element.value))

        return da

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on current location of
        the iterator. Only returns active key/value pairs, doesn't
        return None or tombstones.
        """
        try:
            value = None

            # Iterate until we find an active key/value pair
            while value is None or value.is_tombstone:
                value = self._buckets[self._index]
                self._index += 1

        except DynamicArrayException:  # index is out of bounds
            raise StopIteration

        return value

    def _find_initial_index(self, key: str) -> int:
        """
        Helper function to compute the initial index for an element.
        """
        return self._hash_function(key) % self.get_capacity()

    def _find_quad_index(self, initial_index: int, j: int) -> int:
        """
        Helper function to compute the index using quadratic probing.
        Has the formula i = i_initial + j^2 (where j = 1, 2, 3, ...)
        """
        return (initial_index + (j ** 2)) % self.get_capacity()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
