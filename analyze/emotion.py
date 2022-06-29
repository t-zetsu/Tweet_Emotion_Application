from mlask import MLAsk
import glob
import json
import re
import os
import argparse

def remove(str):
	#URLの除去
	str = re.sub(r"http\S+", "", str)
	#メンションの除去
	str = re.sub(r"@(\w+) ", "", str)
	#RTの除去
	str = re.sub(r"RT @(\w+): ", "", str)
	#改行文字の除去
	str = re.sub("\n", "", str) 
	return str

def tweet_to_emotion(tweet_data, emotion_analyzer):
	if args.emoji:
		emoji_dic = json.load(open("../data/emoji/emoji.json","r"))
		emoji_pattern = re.compile('|'.join(emoji_dic.keys()))
	emotion_dic = {}
	for key in tweet_data: #各トレンド
		emotion_dic[key] = []
		for tweet in tweet_data[key]: #各ツイート
			#余計な文字列の除去
			tweet = remove(tweet)
			#絵文字変換
			if args.emoji:
				tweet = emoji_pattern.sub(lambda x: emoji_dic[x.group()], tweet)
			#感情分析
			result = emotion_analyzer.analyze(tweet)
			if result["emotion"]:
				emotion = list(result["emotion"])
			else:
				emotion = [str(result["emotion"])] #None
			emotion_dic[key].append({"tweet":tweet, "emotion":emotion})
	return emotion_dic

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--emoji', action='store_true', help="Converting emoji into emotional expressions")
	parser.add_argument('--input', default='../data/currentTrend.json', type=str, help='Input file for tweet data')
	parser.add_argument('--output', default='../data/outputs/currentEmotion.json', type=str, help='Output file for tweet data')

	return parser.parse_args()

def main():
	#モデルの読み込み
	emotion_analyzer = MLAsk('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')	

	#データの読み込み
	# tweet_data_path = glob.glob('../data/*.json')
	# tweet_data = json.load(open(tweet_data_path[-1],'r'))
	tweet_data = json.load(open(args.input,'r'))

	#分析
	emotion_dic = tweet_to_emotion(tweet_data, emotion_analyzer)

	#結果の書き込み
	os.makedirs("../data/outputs", exist_ok=True)
	with open(args.output, 'w') as f:
		json.dump(emotion_dic, f, ensure_ascii=False)


if __name__ == "__main__":
	args = get_args()
	main()