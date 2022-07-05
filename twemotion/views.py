#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
from analyze.emotion import main as emotion_analysis
from analyze.getTrendingTweets import main as get_trend
import json
import time


def index(request):
    #twitterデータ取得＆感情分析
    with open('twemotion/GetTime.log', 'r') as f_read:
        data = f_read.read()
    GetTime = float(data) if data!="" else 0 #最新取得時刻
    NowTime = time.time() #現時刻
    if (NowTime-GetTime>=900): #最新取得時刻より15分以上経っていたら取得
        get_trend()
        emotion_analysis()
        with open("twemotion/GetTime.log","w") as f_write: #最新取得時刻を更新
            f_write.write(str(NowTime))
    
    #感情分析結果を読み込み
    with open("data/outputs/currentEmotion.json", "r") as json_open:
        json_load = json.load(json_open)
    json_load = {key.replace("#",""):value for key, value in json_load.items()}
    print(json_load)
    trend_url = {}
    for trend in json_load.keys(): #各トレンドページのURLを追加
        trend_url[trend] = "http://127.0.0.1:8000/twemotion/trend?t="+trend;
    context = {"trend_url":trend_url}
    return render(request, 'twemotion/index.html', context)
    

def trend(request):
    #URLパラメータを取得
    none = False
    if 't' in request.GET: #トレンド名
        t = request.GET['t']
    if 'none' in request.GET: #Noneを表示するか
        none = request.GET['none']=='1'
        
    #感情分析結果を集約
    with open("config/emotion_display.json", "r") as color_json_open: #各感情に関する設定ファイル読み込み
        emotion_dic = json.load(color_json_open)
    with open("data/outputs/currentEmotion.json", "r") as analysis_json_open: #分析結果読み込み
        analysis_result = json.load(analysis_json_open)
    analysis_result = {key.replace("#",""):value for key, value in analysis_result.items()}
    for tweet in analysis_result[t]:
        for em in tweet["emotion"]:
            emotion_dic[em]["point"] += 100 / (len(analysis_result[t]) * len(tweet["emotion"])) #100 / (ツイート数 * 感情数)をインクリメント
            emotion_dic[em]["tweet"].append({"content":tweet["tweet"], "url":tweet["url"]}) #該当ツイートを追加

    #ポイントの正規化
    if (not(none)): #Noneを表示しない場合
        emotion_dic.pop('None')
        point_sum = 0
        for k, v in emotion_dic.items():
            point_sum += v['point']
        for k in emotion_dic.keys():
            emotion_dic[k]['point'] *= 100 / point_sum
    
    #丸め&ソート
    for em, content in emotion_dic.items():
        content["point"] = round(content["point"], 3) #丸め
    emotion_dic = sorted(emotion_dic.items(), key=lambda x:x[1]["point"], reverse=True) #感情ポイントが多い順にソート
    emotion_dic = {item[0]:item[1] for item in emotion_dic if item[1]["point"]!=0}
    
    #None切り替えボタンに関する辞書
    none_mode = {}
    none_mode["url"] = "http://127.0.0.1:8000/twemotion/trend/?t=" + t #埋め込みURL
    none_mode["url"] += "&none=0" if none else "&none=1"
    none_mode["alt"] = "「無」を表示" #altの内容
    none_mode["alt"] += "しない" if none else "する"
    
    context = {"name":t, "none_mode":none_mode, "result":emotion_dic}
    return render(request, 'twemotion/trend.html', context)