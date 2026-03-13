class Solution:
    def bellmanFord(self, V, edges, src):
        dist = [float('inf')] * V
        dist[src] = 0

        # Relax edges V-1 times
        for _ in range(V - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True

            if not updated:
                break

        # Check for negative cycle
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                return [-1]

        return dist


if __name__ == "__main__":
    sol = Solution()

    # Test Case 1
    V = 3
    edges = [
        [0, 1, 1],
        [1, 2, 3],
        [0, 2, 6]
    ]
    src = 0
    print("Test 1:", sol.bellmanFord(V, edges, src))
    assert sol.bellmanFord(V, edges, src) == [0,1,4]
    # Expected: [0,1,4]

    # Test Case 2 (negative edge but no cycle)
    V = 4
    edges = [
        [0,1,4],
        [0,2,5],
        [1,2,-3],
        [2,3,4]
    ]
    src = 0
    print("Test 2:", sol.bellmanFord(V, edges, src))
    assert sol.bellmanFord(V, edges, src) == [0,4,1,5]
    # Expected: [0,4,1,5]

    # Test Case 3 (negative cycle)
    V = 3
    edges = [
        [0,1,1],
        [1,2,-1],
        [2,0,-1]
    ]
    src = 0
    print("Test 3:", sol.bellmanFord(V, edges, src))
    assert sol.bellmanFord(V, edges, src) == [-1]
    # Expected: [-1]