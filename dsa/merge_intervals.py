from typing import List
class Solution:
    # Merge Intervals (LC 56) — sorting
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort()
        current_session = intervals[0]
        sessions = []
        for i in range(1, len(intervals)):
            interval_start, interval_end = intervals[i]
            if interval_start <= current_session[1]:
                current_session[1] = max(interval_end, current_session[1])
            else:
                sessions.append(current_session)
                current_session = [interval_start, interval_end]
        sessions.append(current_session)
        return sessions