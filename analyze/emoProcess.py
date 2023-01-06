import json
import codecs

def main():
    with open("data/outputs/currentEmotion.json", "r") as analysis_json_open:
        analysis_result = json.load(analysis_json_open)
    
    with open("data/tweets/currentTrend.json", "r") as tweet_json_open:
        tweets_result = json.load(tweet_json_open)

    analysis_result = {key.replace(
        "#", ""): value for key, value in analysis_result.items()}
    tweets_result = {key.replace(
        "#", ""): value for key, value in tweets_result.items()}

    trend_emo ={}
    
    

    for t in analysis_result.keys():
        dict_emo = {}
        for (tweet, url) in zip(analysis_result[t], tweets_result[t]):
            del tweet["tweet"]
            tweet.update({"url": url["url"]})
            emotion = tweet["emotion"]
            max_v = max(emotion.values())
            min_v = min(emotion.values())
            for k in emotion.keys():
                emotion[k] = 100*(emotion[k] - min_v) / (max_v - min_v)
                if k not in dict_emo:
                    dict_emo.update({k: emotion[k]})
                else:
                    dict_emo[k] += emotion[k]
            tweet["emotion"] = emotion


            max_v = max(dict_emo.values())
            min_v = min(dict_emo.values())

            for k in dict_emo.keys():
                dict_emo[k] = 100*(dict_emo[k] - min_v) / (max_v - min_v)
            
            total = sum(dict_emo.values())
            for k in dict_emo.keys():
                dict_emo[k] = 100*dict_emo[k] / total
            
            list = sorted(dict_emo.items(), key= lambda x: x[1], reverse=True)
            dict_emo.clear()
            dict_emo.update(list)
            
            
            # print(dict_emo)
            trend_emo.update({t: dict_emo})
            
      

    with codecs.open("./data/outputs/processedEmotion_tweet.json", 'a', 'utf-8') as file:
        file.seek(0)
        file.truncate()
        dict = json.dump(analysis_result, file, ensure_ascii=False)

    with codecs.open("./data/outputs/processedEmotion_trend.json", 'a', 'utf-8') as file1:
        file1.seek(0)
        file1.truncate()
        dict = json.dump(trend_emo, file1, ensure_ascii=False)

if __name__ == "__main__":
    main()
    


