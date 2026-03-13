from typing import List
class Solution:
    # Maximum Subarray (LC 53) — Kadane's Algorithm
    def maxSubArray(self, nums: List[int]) -> int:
        maxSum = nums[0]
        curSum = nums[0]
        for i in range(1, len(nums)):
            curSum = nums[i] + curSum
            if curSum < nums[i]:
                curSum = nums[i]
            maxSum = max(maxSum, curSum)
        return maxSum   