import random
import language
import sys

class MarkovSeed:
    def __init__(self):
        self.hashtags = []
        self.users = []
        self.source_account = ''

def markov_tweet(tweets, hashtag, prefix='', suffix='', reply=''):

    count = 0
    table = {}
    start = {}
    
    table, start = build_chain(tweets)

    message1, count1 = generate_message(table, start, hashtag, reply = reply, prefix = prefix, suffix = suffix)
    message2, count2 = generate_message(table, start, hashtag, reply = reply, prefix = prefix, suffix = suffix)
    message3, count3 = generate_message(table, start, hashtag, reply = reply, prefix = prefix, suffix = suffix)

    if count1 > count2 and count1 > count3:
        return message1
    elif count2 > count1 and count2 > count3:
        return message2
    else:
        return message3

def build_chain(tweets):
    nonword = "\n" 
    w1 = nonword
    w2 = nonword
    # GENERATE TABLE
    table = {}
    start = {}
    for line in tweets:
        for index, word in enumerate(line.split()):
            if word == '&amp;':
                word = '&'
            elif word == '&gt;':
                word = '>'
            elif word == '&lt;':
                word = '<'
                        
            if index == 1:
                start.setdefault(line.split()[0],word)
            
            table.setdefault((w1,w2),[])

            if any(entry == word for entry in table[(w1,w2)]):            
                w1, w2 = w2, word                
                continue
            else:
                table[(w1,w2)].append(word)
            w1, w2 = w2, word

    return table,start

def generate_message(table, start, hashtag, prefix='', suffix='', reply=''):

    w1 = random.choice(list(start.keys()))
    w2 = start[w1]

    output = w1.capitalize() + ' ' + w2
    output_temp = output
    count = 0
    total_chain_len = 0
    count_chain = 0
    chain_len = 0

    while len(output + '      ' + hashtag + reply + prefix + suffix) < 140 and count < 1000:
        
        output = output_temp
        #if tweet is long enough, end on complete sentences
        if len(output) > 30 and output.rstrip().endswith(tuple([".","!","?"])):
            break
        
        try:
            w1, w2, newword = new_word_weighted_non_twitter(table, w1, w2)
            count += 1
            count_chain += 1
            chain_len += len(table[(w1,w2)])
            total_chain_len += len(table[(w1,w2)])
        except:
            seed = random.choice(list(table.keys()))
            newword = w1
            count_chain = 0
            chain_len = 0

        output_temp += ' ' + newword
        w1, w2 = w2, newword

        #if markov chain has few options, reseed
        if count_chain > 4 and chain_len < count_chain + 4:
            count_chain = 0
            chain_len = 0
            w1 = random.choice(list(start.keys()))
            w2 = start.pop(w1)
            output_temp += random.choice(['!','.','?',',','','','','','']) + ' ' + w1 + ' ' + w2
        
       
    
    output = output.lstrip()
    if not output.rstrip().endswith('.') and not output.endswith('?') and not output.endswith('!'):
        output = output.rstrip() + random.choice(['!','.','?']) + ' '
    message = prefix + output[0].capitalize() + output[1:] + suffix + ' ' + hashtag
    return language.sanitize_language(message), total_chain_len



def new_word_weighted_non_twitter(table, w1, w2):
    try:
        newword = random.choice(table[(w1, w2)])
    except:
        w1, w1 = new_seeds(table)

    if ((newword.startswith('#') or newword.startswith('@') or newword.startswith('RT') or newword.startswith('http')) and random.randrange(1,100) < 90):
        seed = random.choice(list(table.keys()))
        w1, w2 = new_seeds(table)
        newword = random.choice(table[(w1, w2)])

    return w1, w2, newword

def new_seeds(table):
     seed = random.choice(list(table.keys()))
     w1 = seed[0]
     w2 = seed[1]
     return w1, w2