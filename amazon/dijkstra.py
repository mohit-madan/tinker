def shortest_path(n: int, edges: list[list[int]], src: int, dst: int) -> int:
    """
    Finds the minimum cost to travel from src to dst.
    
    Args:
    n: int - The number of nodes in the graph (0 to n-1).
    edges: List[List[int]] - A list of directed edges [u, v, weight].
    src: int - The starting node.
    dst: int - The destination node.
    
    Returns:
    int - The minimum cost to reach dst, or -1 if unreachable.
    """
    # Your standard Dijkstra implementation here
    pass


# ==========================================
# TEST CASES FOR QUESTION 1
# ==========================================

if __name__ == "__main__":
    # Test Case 1: Standard shortest path
    # 0 -> 1 costs 100
    # 1 -> 2 costs 100
    # 0 -> 2 costs 500 (Direct route is more expensive than going through 1)
    edges1 = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert shortest_path(3, edges1, 0, 2) == 200, "Q1 Test Case 1 Failed"

    # Test Case 2: Unreachable destination
    edges2 = [[0, 1, 100], [2, 3, 200]]
    assert shortest_path(4, edges2, 0, 3) == -1, "Q1 Test Case 2 Failed"

    # Test Case 3: Longer chain
    edges3 = [[0, 1, 10], [1, 2, 10], [2, 3, 10], [0, 3, 50]]
    assert shortest_path(4, edges3, 0, 3) == 30, "Q1 Test Case 3 Failed"
    
    print("All Q1 test cases passed!")