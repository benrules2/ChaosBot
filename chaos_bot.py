import twitter_bot as t
import random
import markov
import sys

if __name__ == "__main__":
    bot = t.account()
    
    seeds = bot.retrieve_seeds_for_bot("@mayhem_bot", minutes = 6, max = 2)
    
    if len(sys.argv) > 1 and len(seeds) == 0:
        seed = markov.MarkovSeed()
        words = sys.argv[1].split()    

        for word in words:
            if(word.startswith("#")):
                seed.hashtags.append(word.replace("?", "").replace(".", ""))
            elif(word.startswith("@")):
               seed.users.append(word.replace("@", "").replace(".", "").replace("!","").replace("?","").replace(",",""))
        
        seeds.append(seed)

    if len(seeds) == 0 and random.randrange(1,100) > 96:
        bot.markov_tweet_from_queries(bot.get_trending_hashtag())
    
    for seed in seeds:
        bot.markov_tweet_from_queries(seed)


