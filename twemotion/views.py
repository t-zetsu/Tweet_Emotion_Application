#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
import analyze.emotion as emt
import json
import time


def index(request):
    #twitterデータ取得＆感情分析
    with open('twemotion/GetTime.log', 'r') as f_read:
        data = f_read.read()
    GetTime = float(data) if data!="" else 0 #最新取得時刻
    NowTime = time.time() #現時刻
    if (NowTime-GetTime>=900): #最新取得時刻より15分以上経っていたら取得
        emt.emotion_analysis()
        with open("twemotion/GetTime.log","w") as f_write: #最新取得時刻を更新
            f_write.write(str(NowTime))
    
    #感情分析結果を読み込み
    with open("analyze/result.json", "r") as json_open:
        json_load = json.load(json_open)
    
    trend_url = {}
    for trend in json_load.keys(): #各トレンドページのURLを追加
        trend_url[trend] = "http://127.0.0.1:8000/twemotion/trend?t="+trend;
    context = {"trend_url":trend_url}
    return render(request, 'twemotion/index.html', context)
    

def trend(request):
    #感情カラー
    emotion_color = {
        "iya":"#daa520",
        "yorokobi":"#ff8c00",
        "kowa":"#000080",
        "yasu":"#008000",
        "suki":"#ff69b4",
        "aware":"#4682b4",
        "ikari":"#800000",
        "odoroki":"#9400d3",
        "takaburi":"#ff0000",
        "haji":"#c71585",
        "None":"#696969"
    }
    
    #URLパラメータを取得
    if 't' in request.GET:
        t = request.GET['t']
    
    #感情分析結果を集約
    with open("analyze/result.json", "r") as json_open: #分析結果読み込み
        json_load = json.load(json_open)
    emotion_summary = {} #分析結果を集約したもの（各感情の百分率を示す）
    for tweet in json_load[t]:
        for em in tweet["emotion"]:
            if em not in emotion_summary.keys(): #未登録の感情の場合追加
                emotion_summary[em] = 0
            emotion_summary[em] += 100 / (len(json_load[t]) * len(tweet["emotion"])) #100 / (ツイート数 * 感情数)をインクリメント
    emotion_summary = sorted(emotion_summary.items(), key=lambda x:x[1], reverse=True) #感情ポイントが多い順にソート
    
    context = {"name":t, "tweets":json_load[t], "analysis":emotion_summary, "emcolor":emotion_color}
    return render(request, 'twemotion/trend.html', context)