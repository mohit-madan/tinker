import hashlib
from collections import OrderedDict
import threading 

class TTLCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def _make_key(self, tenant_id, model, prompt):
        normalized = " ".join(prompt.strip().split()).lower()
        prompt_hash = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        return (tenant_id, model, prompt)
    
    def set(self, tenant_id, model, prompt, value, ttl_seconds):
        expiry = time.time() + ttl_seconds
        key = self._make_key(tenant_id, model, prompt)
        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
            
            elif len(self.cache) >= self.max_size:
                self.cache.popitem(last = False) ## remove lru

            self.cache[key] = (value, expiry)

    def get(self, key):
        key = self._make_key(tenant_id, model, prompt)
        with self.lock:
            item = self.store.get(key)
            if item is None:
                return None
            
            value, expiry = self.cache[key]
            if time.time() > expiry:
                del self.store[key]
                return -1
            
            self.cache.move_to_end(key)
            return value

    def delete(self, tenant_id, model, prompt):
        key = self._make_key(tenant_id, model, prompt)
        self.cache.pop(key, None)