# dynamic_sharding_using_consistent_hashing
Here, I implemented dynamic database sharding using consistent hashing. But we can shard cache, server instead of database.

---

## 🧩 What is Consistent Hashing?

Imagine you have a **sharded database** (say 4 shards). Normally, you might use `hash(key) % num_shards` to decide where to store a user’s data.
But there’s a problem:

* If you add/remove a shard, **all keys get remapped** because `num_shards` changes. That’s very expensive.
* Consistent hashing solves this by arranging shards and keys on a **hash ring**.

### Key Ideas:

1. **Ring (0–2³²):** We treat the hash space as a circle.
2. **Shard placement:** Each shard gets placed on the circle at multiple points (called **virtual nodes**) to balance load.
3. **Key placement:** A key is hashed and mapped clockwise to the nearest shard.
4. **Minimal rehashing:** When a shard is added/removed, only nearby keys move, not all keys.
5. **virtual nodes minimize key shifting and balance load
6. **Also, we can implement replication for high availability, distribute read and write (Instead of store data one shart we can store multiple shard clockwise.).

---

## 🔑 Key Points You Should Notice:

* **Virtual nodes (replicas):** Prevents imbalance when one shard gets too many keys.
* **Minimal remapping:** Adding/removing a shard only affects part of the ring.
* **Bisect module:** Efficiently finds the shard using binary search in `O(log N)`.

---

👨‍🏫 Mentor Question for You:
If we didn’t use **virtual nodes** and just placed one shard per position, what problem could occur? Would you like me to show you a demo of this imbalance with some graphs?

