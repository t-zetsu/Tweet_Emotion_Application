import json
import time
import requests
#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
from django.conf import settings
#from analyze.emotion import main as emotion_analysis
#from analyze.getTrendingTweets import main as get_trend


def index(request):
    #twitterデータ取得＆感情分析
    """
    with open('twemotion/GetTime.log', 'r') as f_read:
        data = f_read.read()
    GetTime = float(data) if data!="" else 0 #最新取得時刻
    NowTime = time.time() #現時刻
    if (NowTime-GetTime>=900): #最新取得時刻より15分以上経っていたら取得
        get_trend()
        emotion_analysis()
        with open("twemotion/GetTime.log","w") as f_write: #最新取得時刻を更新
            f_write.write(str(NowTime))
    """
    
    #感情分析結果(ツイートごと)を読み込み
    with open("data/tweets/processedEmotion_trend.json", "r") as json_open:
        json_load = json.load(json_open)
    trend_url = {}
    for trend in json_load.keys(): #各トレンドページのURLを追加
        trend_removeTag = trend.replace("#","")
        trend_url[trend_removeTag] = "http://127.0.0.1:8000/twemotion/trend?t="+trend_removeTag;
    context = {"trend_url":trend_url}
    return render(request, 'twemotion/index.html', context)
    

def trend(request):
    #各感情ごとで表示する最大ツイート数
    display_tweetnum = 10
    
    #URLパラメータ（トレンド名）を取得
    if 't' in request.GET:
        t = request.GET['t']
    
    #感情分析結果をソート
    with open("data/tweets/processedEmotion_trend.json", "r") as trend_json_open: #感情分析結果(トレンドごと)を読み込み
        analysis_trend = json.load(trend_json_open)
    analysis_trend = {key.replace("#",""):value for key, value in analysis_trend.items()}
    emotion_ranking = sorted(analysis_trend[t].items(), key=lambda x:x[1], reverse=True) #感情ポイントが多い順にソートした感情集合
    emotion_ranking = {key:round(value, 3) for key, value in emotion_ranking} #ポイント丸め
    
    #円グラフ表示に関する辞書
    with open(str(settings.MEDIA_ROOT) + "/config/emotion_display.json", "r") as color_json_open: #各感情に関する設定ファイル読み込み
        emotion_color = json.load(color_json_open)
    pie_chart = {"label":[], "color":[], "point":[]}
    for em, point in emotion_ranking.items():
        pie_chart["label"].append(emotion_color[em]["japanese"])
        pie_chart["color"].append(emotion_color[em]["color"])
        pie_chart["point"].append(point)
    
    #該当ツイート表示に関する辞書
    tweets = {em:{"label":emotion_color[em]["japanese"], "color":emotion_color[em]["color"], "tweet":[], "point":point} for em, point in emotion_ranking.items()}
    with open("data/tweets/processedEmotion_tweet.json", "r") as tweet_json_open: #感情分析結果(ツイートごと)を読み込み
        analysis_tweet = json.load(tweet_json_open)
    analysis_tweet = {key.replace("#",""):value for key, value in analysis_tweet.items()}
    tweet_emotion = analysis_tweet[t] #各ツイートとその感情割合
    for em in tweets.keys():
        #tweet_emotion_point = {tweet["tweet"]:tweet["emotion"][em] for tweet in tweet_emotion if max(tweet["emotion"].items(), key=lambda x:x[1])[0] == em} #各ツイートの感情emのポイント（emが最大ポイントとなるツイートのみ厳選）（最上位の感情しかツイート表示されないため，最大ポイントの縛りはなしの方が良さげか）
        tweet_emotion_point = {tweet["url"]: tweet["emotion"][em]/sum(tweet["emotion"].values()) for tweet in tweet_emotion} #各ツイートの感情emのポイント割合
        tweet_emotion_point = sorted(tweet_emotion_point.items(), key=lambda x:x[1], reverse=True) #感情emのポイント割合が多い順にソート
        #tweets[em]["tweet"] = [tweet[0] for tweet in tweet_emotion_point[0:min(display_tweetnum,len(tweet_emotion_point))]] #上位display_tweetnum個を取り出す
        tweets[em]["tweet"] = [tweet[0] for tweet in tweet_emotion_point[0:min(display_tweetnum,len(tweet_emotion_point))]] #key(ツイートURL）のみをtweetに保存
        
    #tweetsのtweetのkeyの中身を埋め込みコードにする
    embed_codes = {} #URLと埋め込みコードの対応辞書
    for key, value in tweets.items():
        tweet_codes = [] #tweetと置き換える埋め込みコード集合
        for tweet_url in value["tweet"]:
            if tweet_url in embed_codes.keys(): #tweet_urlが既に登録されている場合，読み込み
                tweet_codes.append(embed_codes[tweet_url])
            else: #未登録の場合，取得
                r = requests.get("https://publish.twitter.com/oembed?url=" + tweet_url)
                if "json" in r.headers.get("content-type"): #JSONとして読み込むことができる場合のみ追加
                    oembed_json = json.loads(r.text)
                    print(oembed_json)
                    if ("html" in oembed_json): #全員が見ることのできるツイートのみ追加
                        embed_codes[tweet_url] = oembed_json["html"]
                        tweet_codes.append(oembed_json["html"])
            if len(tweet_codes) == display_tweetnum: #最大表示ツイート数に達した場合，ツイートの走査をやめる
                break
        tweets[key]["tweet"] = tweet_codes #埋め込みコードに置き換え
    
    context = {"name":t, "pie_chart":pie_chart, "tweets":tweets}
    return render(request, 'twemotion/trend.html', context)