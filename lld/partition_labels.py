# Version A: Function to partition labels
# Problem Statement: 
# You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part.
# Return a list of integers representing the size of each partition.
# Example:
# Input: s = "abacaba"
# Output: [3, 1, 1, 3]
# Explanation:
# The partition is "aba" and "cab".
# The first part is "aba" because it contains the letter 'a' only once.
# The second part is "cab" because it contains the letter 'c' only once.
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        end = {}
        for i in range(len(s)):
            end[s[i]] = i
        result = []
        partition_start = 0
        partition_end = 0
        for i in range(len(s)):
            partition_end = max(end[s[i]], partition_end)
            if partition_end == i:
                result.append(partition_end - partition_start + 1)
                partition_start = i + 1
        
        return result