from collections import defaultdict
from typing import List
class Solution:
    # Task Scheduler (LC 621) — greedy
    def leastInterval(self, tasks: List[str], n: int) -> int:
        taskCount = defaultdict(int)
        
        for task in tasks:
            taskCount[task] += 1
        
        max_freq = max(taskCount.values())
        max_count = 0
        for v in taskCount.values():
            if v==max_freq:
                max_count+=1
        
        return max((max_freq-1)*(n+1)+max_count, len(tasks))