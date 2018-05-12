import json

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from utils.wrappers import Twitter, ToneAnalyzer, Translator
from utils.brands import BrandsDetector

app = Flask(__name__)


def _get_tweets(username, n=None, brands=False, filter_by_brands=False, tone=False, translate=False):
    tweets = []
    for text in twitter.get_texts(username, n):
        tweet = {'text': text}
        if brands:
            tweet['brand'] = brand_detector.find(text)
            if filter_by_brands and tweet['brand'] == '-':
                continue
        if translate:
            text = trans.translate(text)
        if tone:
            tweet['tones'] = tone_analyzer.analyze(text)
        tweets.append(tweet)
    return pd.DataFrame(tweets)


# def _get_tweets_summary(username, n=None):
#     tweets = _get_tweets(username, n, True, True, True, True)
#
#     brands_tweets = defaultdict(list)
#     for t in tweets:
#         if t['brand'] != '-':
#             brands_tweets[t['brand']].append(t)
#
#     summary = {}
#     distribution = {'names': [], 'counts': []}
#     for brand in brands_tweets:
#         sum_tones = defaultdict(float)
#         for t in brands_tweets[brand]:
#             for tone in t['tones']:
#                 sum_tones[tone] += t['tones'][tone]
#         n = len(brands_tweets[brand])
#         mean_tones = {k: v/n for k, v in sum_tones.items()}
#         summary[brand] = mean_tones
#         distribution['names'].append(brand)
#         distribution['counts'].append(n/len(tweets))
#
#     return {'summary': summary, 'distribution': distribution}


def save_plots(df):
    sns.set_style('whitegrid')
    sns.set_context('poster')

    plt.figure(figsize=(12, 6))
    sns.countplot(df['brand'])
    plt.title('Brands distribution in tweets')
    plt.savefig('static/images/count_distribution.png')

    df.dropna(inplace=True)
    df.index = df['brand']
    df = df['tones'].apply(pd.Series)
    df = df.groupby(df.index).agg(np.median).stack().reset_index()
    df.columns = ['brand', 'tones', 'probability']

    plt.figure(figsize=(12, 6))
    sns.barplot('brand', 'probability', 'tones', df)
    plt.title('Tones distribution in brands')
    plt.savefig('static/images/tones_distribution.png')


# @app.route('/debug', methods=['POST', 'GET'])
# def debug():
#     if request.method == 'GET':
#         return render_template('debug.html')
#     if request.method == 'POST':
#         username = request.form['username']
#         result = _get_tweets(username, 10, tone=True, brands=True, translate=False)
#         return render_template('debug.html', result=result, show_tones=True, show_brand=True)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        username = request.form['username']
        df = _get_tweets(username, 200, True, True, True, True)
        save_plots(df)
        df.to_pickle('./tmp.pkl')
        return render_template('main.html', result=True)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = Twitter(config['twitter'])
    tone_analyzer = ToneAnalyzer(config['tone_analyzer'])
    brands_regex = json.load(open('resources/brands.json', encoding='utf8'))
    trans = Translator()
    brand_detector = BrandsDetector(brands_regex)
    app.run(debug=True)
