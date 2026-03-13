import heapq
class Solution:
    # Prim's Algorithm (LC 1168) — MST
    def spanningTree(self, V, edges):
        # code here
        adj = [[] for _ in range(V)]
        for u,v,w in edges:
            adj[u].append((v,w))
            adj[v].append((u,w))
        
        vis = set()
        pq = [(0,0)]
        res = 0
        while pq:
            dist, node = heapq.heappop(pq)
            if node in vis:
                continue
            vis.add(node)
            res+=dist
            for nei,w in adj[node]:
                if nei not in vis:
                    heapq.heappush(pq, (w, nei))
        return res