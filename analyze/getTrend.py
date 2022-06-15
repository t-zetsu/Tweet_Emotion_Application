import codecs
import json
import os
import tweepy

auth = tweepy.OAuth1UserHandler(
   "iUzLnPTJVekOxQT4WqwSqBnkB",
   "KeFVqzN4o5VcsSx240hanZuBuIsM0naPPU3TJJnWblkcJXu2fU",
   "1529282243629178882-3QUmtyOUud6j40tB5uskY4DphF0qGP",
   "SM4ByRgeds4pWLJnsIY5fY79NRh0woG07zQBkgnOITY3j"
)

api = tweepy.API(auth)


def getTrends(woeid):

    for area, wid in woeid.items():
        trends = api.get_place_trends(wid)[0]

    return trends


def getTweets(keyword):

    print(keyword)
    tweets = tweepy.Cursor(api.search_tweets, q = keyword, lang = 'ja').items(200)

    return tweets


woeid = {
    "Japan": 23424856
}

trends = getTrends(woeid)

keywords = []
for trend in trends["trends"] :
    keywords.append(str(trend['name']))
keywords = keywords[0:10]

path = './data/currentTrend.json'
file = codecs.open(path, 'a', 'utf-8')

cT = {}

tag = 0

if os.path.getsize(path) :
    json_open = open(path, 'r')
    pT = json.load(json_open)
    tag = 1

for keyword in keywords :
    tweets = getTweets(keyword)
    for tweet in tweets :
        text = str(tweet.text)
        # url = str(tweet.entities['urls'][0]['url'])
        cT.setdefault(keyword,[]).append(text)
        # cT.setdefault(keyword,[]).append(url)
    if tag : 
        ptext = pT.get(keyword)
        print(ptext)
        if ptext : 
            for tweet in ptext :
                cT.setdefault(keyword,[]).append(text)
    

file.seek(0)
file.truncate()
dict = json.dump(cT, file, ensure_ascii=False)