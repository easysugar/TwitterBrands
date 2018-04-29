import json

from flask import Flask, render_template, request

from utils.wrappers import Twitter, ToneAnalyzer, Translator
from utils.brands import BrandsDetector

app = Flask(__name__)


def _get_tweets(username, n=None, tone=False, brands=False, translate=False):
    tweets = []
    for text in twitter.get_texts(username, n):
        tweet = {'text': text}
        if translate:
            text = trans.translate(text)
        if tone:
            tweet['tones'] = tone_analyzer.analyze(text)
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


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        username = request.form['username']
        result = _get_tweets(username, 10, tone=True, brands=True, translate=True)
        return render_template('main.html', result=result, show_tones=True, show_brand=True)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = Twitter(config['twitter'])
    tone_analyzer = ToneAnalyzer(config['tone_analyzer'])
    brands_regex = json.load(open('resources/brands.json'))
    trans = Translator()
    brand_detector = BrandsDetector(brands_regex)
    app.run(debug=True)
