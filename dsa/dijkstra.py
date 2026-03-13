import heapq
class Solution:
    # Dijkstra's Algorithm (LC 743) — shortest path
    def dijkstra(self, V, edges, src):
        # code here
        graph = [[] for _ in range(V)]
        for u,v,w in edges:
            graph[u].append((v,w))
            graph[v].append((u,w))
        inf = float('inf')
        dist = [inf]*V
        dist[src] = 0
        pq = [(0,src)]
        # it pushed to queue, doesn't matter its visited or not visited
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue
            
            for neigbour, weight in graph[node]:
                new_dist = d + weight
                if new_dist < dist[neigbour]:
                    dist[neigbour] = new_dist
                    heapq.heappush(pq, (new_dist, neigbour))
        return dist

if __name__ == "__main__":
    edges = [[0,1,100],[1,2,100],[0,2,500]]
    src = 0
    print(Solution().dijkstra(3, edges, src))