#coding: UTF-8
import json
import os
import yaml
import argparse
from requests_oauthlib import OAuth1Session

import util
import model

### main ###
# Twitter Official API has the bother limitation of time constraints,
# you can't get older tweets than a week.
FILEIN_DICT = "./config/default.yml"
ROOT_PATH = os.path.dirname(os.path.abspath(__name__))
joined_path = os.path.join(ROOT_PATH, FILEIN_DICT)
config_path = os.path.normpath(joined_path)

with open(config_path, 'rt') as f:
    text = f.read()
config = yaml.safe_load(text)

twitterAPI = OAuth1Session(
    config['twitter']['consumerKey'],
    config['twitter']['consumerSecret'],
    config['twitter']['accessToken'],
    config['twitter']['accessTokenSecret'])

url = "https://api.twitter.com/1.1/search/tweets.json"

def arg_parse():
    parser = argparse.ArgumentParser(
        description='Request query to twitter api', # display before help about args
        epilog='end', # display after help about args
        add_help=True, # -h/–help option
    )
    parser.add_argument('-s',
                        '--since_id',
                        type=str, # default=str
                        required=False
                        )
    parser.add_argument('-u',
                        '--until',
                        help='The upper bound date (yyyy-mm-aa)',
                        type=str, # default=str
                        required=False
                        )
    parser.add_argument('-q',
                        '--q',
                        help='A query text to be matched',
                        type=str, # default=str
                        required=False
                        )
    parser.add_argument('-m',
                        '--max_id',
                        help='The maximum number of tweets to retrieve',
                        type=int, # default=str
                        required=False
                        )
    parser.add_argument('-g',
                        '--geo',
                        help='geocode to be matched',
                        type=str, # default=str
                        required=False
                        )
    parser.add_argument('-l',
                        '--lang',
                        help='language to be matched',
                        type=str, # default=str
                        default='ja',
                        required=False
                        )
    parser.add_argument('-L',
                        '--locale',
                        help='location to be matched',
                        type=str, # default=str
                        default='ja',
                        required=False
                        )
    parser.add_argument('-o',
                        '--outputFileName',
                        help='A filename to export the results',
                        type=str, # default=str
                        default='output_ot.csv',
                        required=False
                        )
    return parser.parse_args()

query = input('>> ')
params = {
    'q' : query,
    'geocode': '',
    'lang': 'ja',
    'locale': 'ja',
    'result_type': 'mixed',
    'count' : '100',
    'until': '2018-03-02',
    'since_id': '',
    'max_id': '',
    'include_entities': 'True'
}

req = twitterAPI.get(url, params = params)

if req.status_code == 200:
    search_timeline = json.loads(req.text)
    tweetList = []
    for tweetRaw in search_timeline['statuses']:
        tweetResult = model.Tweet(tweetRaw)
        tweetList.append(tweetResult.__dict__)
    if tweetList != []:
        util.CsvOperator.export_csv(tweetList, os.path.join(ROOT_PATH,"csv"), params['q'])
else:
    print("ERROR: %d" % req.status_code)
