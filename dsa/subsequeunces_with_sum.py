# Number of Subsequences that Satisfy the Given Sum Condition (LC 1498) — two pointers
from typing import List
class Solution:
    # Number of Subsequences that Satisfy the Given Sum Condition (LC 1498) — two pointers
    def numSubseq(self, nums: List[int], target: int) -> int:
        i,j = 0,len(nums)-1
        count = 0
        nums.sort()
        mod = 10**9 + 7

        while j>=i:
            if nums[i]+nums[j] <= target:
                count = (count + pow(2, j-i,mod))%mod
                i+=1
            else:
                j-=1
        return count