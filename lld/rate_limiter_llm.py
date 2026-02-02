import time
from collections import defaultdict
import threading


class Tokenbucket:
    def __init__(self, capacity: int, refill_rate_per_second: int):
        self.capacity = capacity
        self.refill_rate_per_second = refill_rate_per_second
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.refill_rate_per_second

        if refill_amount > 0:
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now
      
    
class AILimiter:
    def __init__(self, max_rpm, max_tpm):
        self.rpm_config = (max_rpm, max_rpm/60.0)
        self.tpm_config = (max_tpm, max_tpm/60.0)
        self.user_limits = defaultdict(self.create_buckets)
        self.user_locks = defaultdict(threading.Lock)
        self.dict_lock = threading.Lock()

    def create_buckets(self, user_id):
        return {
            'rpm': Tokenbucket(capacity=self.rpm_config[0], refill_rate_per_second=self.rpm_config[1]),
            'tpm': Tokenbucket(capacity=self.tpm_config[0], refill_rate_per_second=self.tpm_config[1]),
        }

    def allow_request(self, user_id, tokens_needed):
        with self.dict_lock:
            user_lock = self.user_locks[user_id]
            limits = self.user_limits[user_id]

        with user_lock:
            rpm_bucket = limits['rpm']
            tpm_bucket = limits['tpm']
            with rpm_bucket.lock:
                with tpm_bucket.lock:
                    rpm_bucket.refill()
                    tpm_bucket.refill()
                    if rpm_bucket.tokens >= 1 and tpm_bucket.tokens >= tokens_needed:
                        rpm_bucket.tokens -= 1
                        tpm_bucket.tokens -= tokens_needed
                        return True
                    return False