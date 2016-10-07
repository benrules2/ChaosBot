import tweepy
import markov
import datetime
import random
from accounts import twitter_account

class account:
    def __init__(self):
        consumer_key= twitter_account['consumer_key']
        consumer_secret= twitter_account['consumer_secret']
        access_key = twitter_account['access_key']
        access_secret = twitter_account['access_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

    def test_tweet(self,message):
        self.api.update_status(message)

    def custom_message(self,message):
        self.api.update_status(message)

    def tweet_message_with_photo(self, message, file_filename, city_name):
        self.api.update_with_media(file_filename,message)

    def print_tweets_with_hashtag(self, hashtag):
        hashtag_tweets = self.api.search(hashtag, lang = 'en'  , rpp = 10)

        for tweet in hashtag_tweets:
            print (tweet.text)

    def markov_tweet_from_queries(self, seed, force_completion, hashtag_out = '#mayhem_bot', tweet_count = 5000, reply = ''):
        total_seed = len(seed.users) + len(seed.hashtags)
        message_list = []
        
        for hashtag in seed.hashtags:
            try:            
                for tweet in tweepy.Cursor(self.api.search,
                           q=hashtag,
                           count=100,
                           include_entities=True,
                           lang="en").items(tweet_count/total_seed):
                    message_list.append(tweet.text)
            except:
                pass

        for user in seed.users:
            try:
                for tweet in tweepy.Cursor(self.api.user_timeline,id=user,count=100).items(tweet_count/total_seed):
                    message_list.append(tweet.text)
            except:
                pass


        if(len(message_list) > 10):
            prefix = ''
            suffix = ''
            for hashtag in seed.hashtags:
                hashtag_out = hashtag + ' ' + hashtag_out
            if(len(seed.users) > 0):
               prefix, suffix = quote_users(seed.users)     
                    
            message = markov.markov_tweet(message_list, hashtag_out, force_complete = force_completion, prefix = prefix, suffix = suffix) #,reply = '@' + seed.source_account + ':')
            
            if message:
                self.custom_message(trim_to_140(message))

    def retrieve_seeds_for_bot(self, name, minutes = 15, max = 10):
        index = 0
        seeds = [] 

        tweets = self.api.search(q=name, rpp = max)

        for tweet in tweets:
            if (tweet.created_at > datetime.datetime.utcnow() - datetime.timedelta(minutes = minutes)) and tweet.retweeted == False:
                seed = markov.MarkovSeed()
                seed.source_account = tweet.user.screen_name
                
                words = strip_substring(tweet.text, name).split()
                for word in words:
                    if(word.startswith("#")):
                        seed.hashtags.append(word.replace("?", "").replace(".", ""))
                    elif(word.startswith("@")):
                       seed.users.append(word.replace("@", "").replace(".", "").replace("!","").replace("?","").replace(",",""))
                  
                seeds.append(seed)

            if len(seeds) > max:
                return seeds
        return seeds

    def get_trending_hashtag(self, count = 1):
        seed = markov.MarkovSeed()
        trends1 = self.api.trends_place(23424775)
        data = trends1[0]
        # grab the trends
        trends = data['trends']
        # grab the name from each trend
        while len(seed.hashtags) < count:
            hashtag = random.choice(trends)['name']
            if hashtag.startswith('#'):
                seed.hashtags.append(hashtag)
        return seed

def combined_less_than_140(message,message_to_add):
    if len(message + message_to_add) <= 140:
        return True
    else:
        return False

def add_if_less_than_140(message, message_to_add):
    if len(message + message_to_add) <= 140:
        return message + message_to_add
    else:
        return message

def strip_substring(string, substring):
    location = string.find(substring)
    newstring = string[:location] + string[location + len(substring):]
    return newstring

def quote_users(users):
    prefix = "\""
    suffix = "\""
    for user in users:
        prefix += '@' + user + ': '
    return prefix, suffix    

def trim_to_140(message):
    if len(message) >140:
        return message[0:139]
    else:
        return message