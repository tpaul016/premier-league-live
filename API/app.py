from flask import Flask, request
from flask_cors import CORS, cross_origin
from topic_modelling import train_model
import soccer_data_retrieval
import json
import tweet_retrieval

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tweetTopics', methods=['GET'])
def getTweetTopics():
    keyword = request.args.get('keyword')
    date = request.args.get('date')
    tweets = tweet_retrieval.get_tweets(keyword, date)
    result = train_model(tweets)
    return json.dumps(result)

@app.route('/schedule', methods=['GET'])
def getSchedule():
    dateTo = request.args.get('dateTo')
    return soccer_data_retrieval.getSchedule(dateTo)

@app.route('/match', methods=['GET'])
def getMatch():
    matchId = request.args.get('id')
    return soccer_data_retrieval.getMatch(matchId)

@app.errorhandler(Exception)
def http_error_handler(error):
    return error.code

if __name__ == '__main__':
    app.run()