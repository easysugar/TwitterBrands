import json

from flask import Flask, render_template, request

from utils.wrappers import Twitter, ToneAnalyzer
from utils.brands import BrandsDetector

app = Flask(__name__)


def _get_tweets(username, n=None, tone=False, brands=False):
    tweets = []
    for text in twitter.get_texts(username, n):
        tweet = {'text': text}
        if tone:
            tweet['tone'] = tone_analyzer.analyze(text)
        if brands:
            tweet['brands'] = brand_detector.find(text)
        tweets.append(tweet)
    return tweets


@app.route('/api/<username>')
def get_tweets(username):
    tone = request.args.get('tone')
    brands = request.args.get('brands')
    count = request.args.get('count') or 10
    tweets = _get_tweets(username, count, tone, brands)
    return json.dumps(tweets, ensure_ascii=False)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = Twitter(config['twitter'])
    tone_analyzer = ToneAnalyzer(config['tone_analyzer'])
    brands_regex = json.load(open('resources/brands.json'))
    brand_detector = BrandsDetector(brands_regex)
    app.run(debug=True)
