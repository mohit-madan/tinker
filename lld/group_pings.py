# Version A: Function to group pings with max gap given
def group_pings(pings, max_gap):
    if not pings:
        return []
    
    pings.sort() # O(n log n)
    sessions = []

    current_session = [pings[0], pings[0]]

    for i in range(1, len(pings)):
        ping = pings[i]
        last_ping_in_session = current_session[1]

        if ping - last_ping_in_session <= max_gap:
            current_session[1] = ping
        else:
            sessions.append(current_session)
            current_session = [ping, ping]
    
    sessions.append(current_session)
    return sessions

# Version B: Function to merge overlapping intervals
def merge(intervals):
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


pings = [1, 2, 5, 6, 7, 12]
print(group_pings(pings, 2))