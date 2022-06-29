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
woeid = {
    "Japan": 23424856
}


def getTrends(woeid):
    # トレンドを取得する
    for area, wid in woeid.items():
        trends = api.get_place_trends(wid)[0]

    return trends


def getTweets(keyword, n):
    # tweet responseを取得する
    print(keyword)
    tweets = tweepy.Cursor(api.search_tweets, q=keyword,
                           lang='ja', include_entities=True).items(n)

    return tweets


def getTrendingTweets():

    trends = getTrends(woeid)

    # この時点でtop10のトレンドを取得する
    keywords = []
    for trend in trends["trends"]:
        keywords.append(str(trend['name']))
    keywords = keywords[0:10]

    path = './data/currentTrend.json'
    file = codecs.open(path, 'a', 'utf-8')

    cT = {}
    # ./data/currentTrend.jsonにデータがあるかどうかを判断し、あれば読み込み、データをpTに保存
    tag = 0  # 0:currentTrend.jsonにデータがない　1:currentTrend.jsonにデータがある
    if os.path.getsize(path):
        json_open = open(path, 'r')
        pT = json.load(json_open)
        tag = 1

    for keyword in keywords:
        # 各トレンドに対して、tweetを200個取得
        tweets = getTweets(keyword, 200)
        # 取得したtweetのテキストとurlをcTに保存
        for tweet in tweets:
            text = str(tweet.text)
            tweetid = str(tweet.id)
            url = 'https://twitter.com/x/status/' + tweetid
            d = {text: url}
            cT.setdefault(keyword, []).append(d)
        # cTとpTの内容を比較し、もし同じトレンドがあればcTにjoin
        if tag:
            ptext = pT.get(keyword)
            print(ptext)
            if ptext:
                for tweet in ptext:
                    cT.setdefault(keyword, []).append(text)

    return cT


def main():

    cT = getTrendingTweets()

    # currentTrend.jsonのデータを消して、cTのデータをcurrentTrend.jsonに書き込む
    with codecs.open("./data/currentTrend.json", 'a', 'utf-8') as file:
        file.seek(0)
        file.truncate()
        dict = json.dump(cT, file, ensure_ascii=False)
        


if __name__ == "__main__":
    main()
