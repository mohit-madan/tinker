def count_unique_pairs(matrix: list[list[int]], target: int) -> int:
    """
    Finds the number of unique pairs in a 2D matrix that sum to the target.
    
    Args:
    matrix: List[List[int]] - A 2D array of unique integers.
    target: int - The target sum.
    
    Returns:
    int - The number of unique pairs that add up to the target.
    """
    # Your code here
    if not matrix or not matrix[0]:
        return 0
    result = set()
    count = 0
    m,n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if target - matrix[i][j] in result:
                count+=1
            result.add(matrix[i][j])
    return count



# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    # Test Case 1: Standard square matrix
    matrix1 = [
        [1, 2],
        [3, 4]
    ]
    target1 = 5
    # Expected pairs: (1, 4) and (2, 3)
    assert count_unique_pairs(matrix1, target1) == 2, "Test Case 1 Failed"

    # Test Case 2: Rectangular matrix
    matrix2 = [
        [1, 9, 3],
        [7, 5, 8]
    ]
    target2 = 10
    # Expected pairs: (1, 9) and (3, 7)
    assert count_unique_pairs(matrix2, target2) == 2, "Test Case 2 Failed"

    # Test Case 3: No pairs sum to target
    matrix3 = [
        [10, 20],
        [30, 40]
    ]
    target3 = 100
    # Expected pairs: None
    assert count_unique_pairs(matrix3, target3) == 0, "Test Case 3 Failed"

    # Test Case 4: Larger matrix with negative numbers
    matrix4 = [
        [ -1,  0,  1],
        [ -2,  5,  2],
        [ 10,  8, -5]
    ]
    target4 = 0
    # Expected pairs: (-1, 1) and (-2, 2)
    assert count_unique_pairs(matrix4, target4) == 3, "Test Case 4 Failed"

    print("All test cases passed!")