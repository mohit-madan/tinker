import time

class TokenBucket:
    def __init__(self, capacity: int, refill_rate_per_second: float):
        self.capacity = capacity
        self.refill_rate_per_second = refill_rate_per_second
        self.tokens = capacity
        self.last_refill = time.time()

    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.refill_rate_per_second

        if refill_amount > 0:
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now

class AILimiter:
    def __init__(self):
        # We use a standard dict so we can manually handle creation logic
        self.user_buckets = {} 

    def get_user_tier_config(self, user_id):
        """
        Define your logic here for different user limits.
        This could look up a database, a config file, or environment variables.
        """
        # Example Logic:
        if user_id.startswith("pro_"):
            return {
                'rpm': 500,
                'tpm': 100000
            }
        else:
            # Default / Free tier
            return {
                'rpm': 10,
                'tpm': 2000
            }

    def create_buckets(self, user_id):
        # 1. Get the specific limits for this user
        config = self.get_user_tier_config(user_id)
        
        # 2. Calculate rates (per second)
        rpm_rate = config['rpm'] / 60.0
        tpm_rate = config['tpm'] / 60.0

        # 3. Return the specific buckets for this user
        return {
            'rpm': TokenBucket(capacity=config['rpm'], refill_rate_per_second=rpm_rate),
            'tpm': TokenBucket(capacity=config['tpm'], refill_rate_per_second=tpm_rate),
        }

    def allow_request(self, user_id, tokens_needed):
        # 1. Lazy Initialization: Create buckets if they don't exist yet
        if user_id not in self.user_buckets:
            self.user_buckets[user_id] = self.create_buckets(user_id)

        limits = self.user_buckets[user_id]
        rpm_bucket = limits['rpm']
        tpm_bucket = limits['tpm']

        # 2. Refill buckets based on time passed
        rpm_bucket.refill()
        tpm_bucket.refill()

        # 3. Check if we have enough tokens
        # We need 1 token for the request itself (RPM) and N tokens for the content (TPM)
        if rpm_bucket.tokens >= 1 and tpm_bucket.tokens >= tokens_needed:
            rpm_bucket.tokens -= 1
            tpm_bucket.tokens -= tokens_needed
            return True
        
        return False

# --- Usage Example ---

limiter = AILimiter()

# 1. A Free User (uses default logic)
user_free = "user_123"
allowed_free = limiter.allow_request(user_free, tokens_needed=500)
print(f"Free User request allowed: {allowed_free}") 

# 2. A Pro User (starts with 'pro_', triggers higher limits)
user_pro = "pro_user_999"
allowed_pro = limiter.allow_request(user_pro, tokens_needed=500)
print(f"Pro User request allowed: {allowed_pro}")