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

def tweet_to_emotion(tweet_data, emotion_analyzer, args):
	if args.no_emoji:
		emoji_dic = json.load(open("./data/emoji/emoji.json","r"))
		# emoji_dic = json.load(open("data/emoji/emoji.json","r"))
		emoji_pattern = re.compile('|'.join(emoji_dic.keys()))
	emotion_dic = {}
	for key in tweet_data: #各トレンド
		emotion_dic[key] = []
		for tweet in tweet_data[key]: #各ツイート
			text = tweet["tweet"]
			#余計な文字列の除去
			text = remove(text)
			#絵文字変換
			if args.no_emoji:
				text = emoji_pattern.sub(lambda x: emoji_dic[x.group()], text)
			#感情分析
			result = emotion_analyzer.analyze(text)
			if result["emotion"]:
				emotion = list(result["emotion"])
			else:
				emotion = [str(result["emotion"])] #None
			tweet["emotion"] = emotion
			emotion_dic[key].append(tweet)
	return emotion_dic

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--no_emoji', action='store_false', help="Not converting emoji into emotional expressions")
# 	parser.add_argument('--input', default='../data/tweets/currentTrend.json', type=str, help='Input file for tweet data')
# 	parser.add_argument('--output', default='../data/outputs/currentEmotion.json', type=str, help='Output file for tweet data')
	parser.add_argument('--input', default='data/tweets/currentTrend.json', type=str, help='Input file for tweet data')
	parser.add_argument('--output', default='data/outputs/currentEmotion.json', type=str, help='Output file for tweet data')

	return parser.parse_args(args=[])

def emotion_analysis(args):
	#モデルの読み込み
	emotion_analyzer = MLAsk('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
	# emotion_analyzer = MLAsk('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd') #zetsu検証用

	#データの読み込み
	tweet_data = json.load(open(args.input,'r'))
	# tweet_data = json.load(open('../data/tweets/exampleTrend.json','r')) #zetsu検証用

	#分析
	emotion_dic = tweet_to_emotion(tweet_data, emotion_analyzer, args)

	#結果の書き込み
	os.makedirs("./data/outputs", exist_ok=True)
	with open(args.output, 'w') as f:
		json.dump(emotion_dic, f, ensure_ascii=False)
	# with open('../data/outputs/exampleEmotion_noemoji.json', 'w') as f: #zetsu検証用
	# 	json.dump(emotion_dic, f, ensure_ascii=False)

def main():
	print("before args")
	args = get_args()
	print("after args")
	emotion_analysis(args)
	
if __name__ == "__main__":
	main()