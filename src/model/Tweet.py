#coding: UTF-8
from datetime import datetime

class Tweet:

    def __init__(self, tweet):
        self.user_name = tweet['user']['name']
        self.created_at = self._extarct_timestamp(tweet['created_at'])
        self.text = tweet['text']
        self.hashtags = self._extract_hashtag_texts(tweet['entities']['hashtags'])
        self.iso_language_code = tweet['metadata']['iso_language_code']
        self.lang = tweet['lang']
        self.time_zone = self._extract_time_zone(tweet['user']['time_zone'])
        self.retweet_count = tweet['retweet_count']
        self.favorite_count = tweet['favorite_count']

    def _extract_hashtag_texts(self, hashtags):
        ht = []
        for hashtag in hashtags:
            if 'text' in hashtag:
                ht.append(hashtag['text'])
        return ht

    def _extract_time_zone(self, time_zone):
        tz = ''
        if not time_zone is None:
            tz = time_zone
        return tz

    def _extarct_timestamp(self, created_at):
        timestamp = str(datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
        return timestamp.split(" ")[0]
