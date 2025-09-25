import hashlib
import bisect 


class ConsistentHashing:
    def __init__(self, replicas=3):
        """
        replicas: Number of Virtual nodes per shard
        for better distribution.
        """
        self.replicas = replicas
        self.ring = dict() # Map of hash -> shard
        # Sorted list of hashes for binary search (bisect)
        self.sorted_keys = [] 

    def _hash(self, key):
        """
        Compute a hash for a given key using MD5, and 
        convert it into an integer
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_shard(self, shard_id):
        """
        Add a shard into the hash ring with 'replicas'
        virtual nodes.
        """
        for rep_num in range(self.replicas):
            # Virtual node key = shard_id + replica number
            virtual_node_key = f"{shard_id}:{rep_num}"
            hash_val = self._hash(virtual_node_key)

            # Add to ring
            self.ring[hash_val] = shard_id 
            bisect.insort(self.sorted_keys, hash_val)

    def remove_shard(self, shard_id):
        """
        Remove a shard (all it's virtual nodes) from 
        the ring
        """

        for rep_num in range(self.replicas):
            virtual_node_key = f"{shard_id}:{rep_num}"
            hash_val = self._hash(virtual_node_key)

            # Remove from the ring and sorted list
            if hash_val in self.ring:
                del self.ring[hash_val]
                self.sorted_keys.remove(hash_val)
    
    def get_shard(self, key):
        """
        Given a key, return the shard it maps to.
        """
        if not self.ring:
            return None 

        hash_val = self._hash(key)

        # Find position in sorted_keys using binary search
        idx = bisect.bisect(self.sorted_keys, hash_val)

        # Wrap around the ring if needed
        if idx == len(self.sorted_keys):
            idx = 0 # Ring is circular
        
        shard_hash = self.sorted_keys[idx]
        return self.ring[shard_hash]


if __name__ == "__main__":
    ch = ConsistentHashing(replicas=5)

    # Add 3 database shards
    ch.add_shard("DB1")
    ch.add_shard("DB2")
    ch.add_shard("DB3")

    # Map users to shards
    users = ["alice", "bob", "charlie", "david", "eve", "frank"]

    print("Initial shard mapping:")
    for user in users:
        print(f"User {user} -> {ch.get_shard(user)}")
    
    # Now add a new Shard
    print("\nAfter adding DB4")
    ch.add_shard("DB4")
    for user in users:
        print(f"User {user} -> {ch.get_shard(user)}")

    # Remove one shard
    print("\nAfter removing DB2:")
    ch.remove_shard("DB2")
    for user in users:
        print(f"User {user} -> {ch.get_shard(user)}")
