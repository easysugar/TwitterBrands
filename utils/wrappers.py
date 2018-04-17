from twitter import Api

class Twitter:
    def __init__(self, config):
        self.api = Api(**config)

    def _get_texts(self, username, last_id):
        tweets = self.api.GetUserTimeline(screen_name=username, max_id=last_id, count=200,
                                          exclude_replies=True, include_rts=False)
        if not tweets:
            return [], None
        last_id = tweets[-1].id - 1
        texts = [t.text for t in tweets]
        return texts, last_id

    def get_texts(self, username, max_count=None):
        last_id = None
        curr_count = 0
        while True:
            texts, last_id = self._get_texts(username, last_id)
            if not texts:
                break
            curr_count += len(texts)
            if max_count and curr_count > max_count:
                texts = texts[:max_count-curr_count]
            for t in texts:
                yield t
            if max_count and curr_count >= max_count:
                break
