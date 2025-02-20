# My program starts here with the creation of the chaining hash table class.

# Hash table implementation using separate chaining to handle collisions.
class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):  # Does both insert and update from the CSV file
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If not, insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #Search for key in bucket list
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # value
        return None

    #Remove key from hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False

    # Retrieves all keys in the hash table.
    def keys(self):
        keys_list = []
        for bucket in self.table:
            keys_list.extend(kv[0] for kv in bucket)  # Add only the keys to the list
        return keys_list

    # Generator to retrieve all key-value pairs in the hash table.
    def items(self):
        for bucket in self.table:
            for kv in bucket:
                yield kv[0], kv[1]