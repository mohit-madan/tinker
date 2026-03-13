from typing import List, Optional
from collections import deque

# Definition for a Node.
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children

class Solution:
    # N-ary Tree Level Order Traversal (LC 429) — BFS
    def levelOrder(self, root: Node) -> List[List[int]]:
        if root is None:
            return []
        q = deque()
        output = []
        q.append(root)
        while q:
            temp = []
            for _ in range(len(q)):
                node = q.popleft()
                temp.append(node.val)
                for children in node.children:
                    q.append(children)
            output.append(temp)
        return output