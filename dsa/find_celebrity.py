from typing import List
def knows(a: int, b: int) -> bool:
    return True 
class Solution:
    # Find the Celebrity (LC 277) — two pointers
    def findCelebrity(self, n: int) -> int:
        candidate = 0
        for i in range(1, n):
            if knows(candidate, i):
                candidate = i
        for i in range(n):
            if i != candidate and (knows(candidate, i) or not knows(i, candidate)):
                return -1
        return candidate