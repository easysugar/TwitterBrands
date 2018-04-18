import json

from flask import Flask, render_template

from utils import wrappers

app = Flask(__name__)


@app.route('/api/tweets/<username>')
def get_tweets(username):
    result = twitter.get_texts(username, max_count=100)
    result = list(enumerate(result))
    return render_template('tweets.html', username=username, result=result)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = wrappers.Twitter(config['twitter'])
    app.run(debug=True)
