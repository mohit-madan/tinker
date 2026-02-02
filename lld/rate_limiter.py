# Rate limiter
# Functional requirements - identify user by id, ip, api key
# Return proper error headers and status codes
    # Scale:
    # 100 M DAU
    # 1 M rps 

# Non-functional requirements
# Avalibility >> consistency
# low latency rate limit checks (<10ms)
# scalable to 1M rps

# Core entities
# request
# client (ip, userid, ip key)
# rules (100 r/s)
from collections import deque, defaultdict
import time 

# Algo 1: storing timestamps of the last requests but cannot handle sudden bursts
class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)

    def allow_request(self, user_id: str):
        current_time = time.time()
        user_history = self.requests[user_id]

        while user_history and current_time - user_history[0] > self.window_seconds:
            user_history.popleft()

        if len(user_history) < self.limit:
            user_history.append(current_time)
            return True
        return False

# Algo 2: Token bucket logic
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: int):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def refill_tokens(self):
        now = time.time()
        time_since_last_refill = now - self.last_refill
        tokens_to_add = time_since_last_refill * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def allow_request(self, tokens):
        self.refill_tokens()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
        