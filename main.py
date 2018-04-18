import json

from flask import Flask

from utils import wrappers

app = Flask(__name__)


@app.route('/')
def main():
    return "Hi there"


@app.route('/api/tweets')
def get_tweets(username):
    return json.dumps(twitter.get_texts(username), ensure_ascii=False)


if __name__ == '__main__':
    config = json.load(open('resources/config.json'))
    twitter = wrappers.Twitter(config['twitter'])
    app.run(debug=True)
