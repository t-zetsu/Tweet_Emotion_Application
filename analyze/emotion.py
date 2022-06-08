from mlask import MLAsk
import glob
import json
import re

def remove(str):
	#URLの除去
	str = re.sub(r"http\S+", "", str)
	#メンションの除去
	str = re.sub(r"@(\w+) ", "", str)
	#RTの除去
	str = re.sub(r"RT @(\w+): ", "", str) 
	return str

def analyze_emotion(tweet_data, emotion_analyzer):
	emotion_dict = {}
	for key in tweet_data: #各トレンド
		emotion_dict[key] = []
		for tweet in tweet_data[key]: #各ツイート
			#余計な文字列の除去
			tweet = remove(tweet)
			result = emotion_analyzer.analyze(tweet)
			if result["emotion"]:
				emotion = list(result["emotion"])
			else:
				emotion = [str(result["emotion"])] #None
			emotion_dict[key].append({"tweet":tweet, "emotion":emotion})
	return emotion_dict

def tweet_to_emotion():
	#モデルの読み込み
	emotion_analyzer = MLAsk('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')	

	#データの読み込み
	tweet_data_path = glob.glob('../data/*.json')
	tweet_data = json.load(open(tweet_data_path[-1],'r'))

	#分析
	emotion_dict = analyze_emotion(tweet_data, emotion_analyzer)

	return emotion_dict

def main():
	# 感情分析
	emotion_dict = tweet_to_emotion()

	#結果の書き込み
	with open("result.json", 'w') as f:
		json.dump(emotion_dict, f, ensure_ascii=False)


if __name__ == "__main__":
	main()