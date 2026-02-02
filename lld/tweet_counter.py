from collections import defaultdict
class TweetCounts:

    def __init__(self):
        self.tweet_map = defaultdict(list)
        self.is_sorted = defaultdict(bool)
    
    def record_tweet(self, tweet_name: str, time: int):
        self.tweet_map[tweet_name].append(time)
        self.is_sorted[tweet_name] = False

    def getTweetCountsPerFrequency(self, freq, tweet_name, start_time, end_time):
        if tweet_name not in self.tweet_map:
            return []
        
        times = self.tweet_map[tweet_name]

        if not self.is_sorted[tweet_name]:
            times.sort()
            self.is_sorted[tweet_name] = True

        if freq == "minute":
            delta = 60
        elif freq == "hour":
            delta = 3600
        elif freq == "day":
            delta = 86400

        # Create the result buckets
        num_buckets = ((end_time - start_time) // delta) + 1
        result = [0] * num_buckets
        
        low, high = 0, len(times)
        while low < high:
            mid = (low + high) // 2
            if times[mid] < start_time:
                low = mid+1
            else:
                high = mid
        
        start_index = low

        for i in range(start_index, len(times)):
            t = times[i]

            if t > end_time:
                break

            bucket_index = (t - start_time) // delta
            result[bucket_index] += 1

        return result