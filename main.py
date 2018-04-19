import json

from flask import Flask, render_template

from utils import wrappers

app = Flask(__name__)


@app.route('/api/tweets/<username>')
def get_tweets(username):
    result = []
    for i, text in enumerate(twitter.get_texts(username, max_count=10)):
        item = {'text': text}
        for name, score in tone_analyzer.analyze(text).items():
            item[name] = '%.2f' % score
        result.append((i, item))
    return render_template('tweets.html', username=username, result=result)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = wrappers.Twitter(config['twitter'])
    tone_analyzer = wrappers.ToneAnalyzer(config['tone_analyzer'])
    app.run(debug=True)
