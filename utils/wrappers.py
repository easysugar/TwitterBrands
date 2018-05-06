import re
import requests
import json

import twitter
import googletrans


class Twitter:
    def __init__(self, config):
        self.api = twitter.Api(**config)

    def _get_texts(self, username, last_id):
        tweets = self.api.GetUserTimeline(screen_name=username, max_id=last_id, count=200,
                                          exclude_replies=True, include_rts=False)
        if not tweets:
            return [], None
        last_id = tweets[-1].id - 1
        texts = [t.full_text for t in tweets]
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


class ToneAnalyzer:
    URL = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone'

    def __init__(self, config):
        self.auth = (config['username'], config['password'])

    def _send_request(self, text):
        headers = {'Content-Type': 'application/json'}
        params = [('version', '2016-05-19')]
        data = json.dumps({'text': text})
        response = requests.post(self.URL,
                                 headers=headers,
                                 params=params,
                                 data=data.encode('utf8'),
                                 auth=self.auth)
        return response

    def _extract_response(self, response):
        if response.status_code != 200:
            return None
        response = response.json()
        tones = response['document_tone']['tone_categories'][0]['tones']
        tones = {t['tone_name']: t['score'] for t in tones}
        return tones

    def analyze(self, text):
        response = self._send_request(text)
        tones = self._extract_response(response)
        return tones


class Translator:
    def __init__(self):
        self.trans = googletrans.Translator()
        self.unsupported_pattern = re.compile(
            "[^\u0000-\u007e\u0400-\u0500]+",
            flags=re.UNICODE)

    def remove_unsupported(self, text):
        return self.unsupported_pattern.sub('', text)

    def translate(self, text):
        text = self.remove_unsupported(text)
        return self.trans.translate(text).text
