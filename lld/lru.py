class Node:
    def __init__(key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        prev, next = node.prev, node.next
        prev.next = node.next
        next.prev = prev
    
    def _add_to_end(self, node):
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node
    
    def get(self, key:int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]

        self._remove(node)
        self._add_to_end(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(key)
        
        node = Node(key, value)
        self.cache[key] = value
        self._add_to_end(node)
        
        if len(self.cache) > capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
