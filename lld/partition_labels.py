# Version A: Function to partition labels
# Problem Statement: 
# You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part.
# Return a list of integers representing the size of each partition.
# Example:
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