from collections import defaultdict, deque
from typing import List
class Solution:
    # Course Schedule II (LC 210) — topological sort
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        nodeCount = defaultdict(int)
        adj = [[] for _ in range(numCourses)]
        for a,b in prerequisites:
            adj[b].append(a)
            nodeCount[a]+=1
        q = deque()
        for i in range(numCourses):
            if i not in nodeCount.keys():
                q.append(i)
        result = []
        while q:
            node = q.popleft()
            result.append(node)
            for item in adj[node]:
                nodeCount[item] -=1
                if nodeCount[item] == 0:
                    q.append(item)
        if len(result) < numCourses:
            return []
        return result