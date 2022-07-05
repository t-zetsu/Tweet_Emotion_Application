 # Tweet_Emotion_Application
Multi Media Engineering Exercise

## 準備
### 環境
1. Dockerfileからイメージを作成
```
docker build -t [IMAGE_NAME] .
```
2. イメージからコンテナを立ち上げる
```
docker run -it -d --ipc=host -v work --name [CONTAINER_NAME] [IMAGE_NAME] /bin/bash
```
3. コンテナを有効化
```
docker exec -it [CONTAINER_NAME] bash
```
(補足)
* Dockerfileがあるところで実行
* pythonのライブラリはrequirements.txtに記載

### 辞書のダウンロード
形態素解析エンジンMeCabと共に使う単語分かち書き辞書[mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)のダウンロードが必要
```
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd #mecab-ipadic-neologd/libexec/install-mecab-ipadic-neologd.shの76行目のsudoを消す必要あり？
./bin/install-mecab-ipadic-neologd -n
echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
# echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
```

## 実行（舌）
### 例
```
cd analyze
python3 emotion.py
```
(補足)
* data/tweets/にあるjsonファイルのツイートを分析
* data/outputs/にjsonファイルが出力される
```
python3 emotion.py --input ../data/tweets/exampleTrend.json --output ../data/outputs/exampleEmotion.json
```

## 実行（加藤）
### 例
```
python3 manage.py runserver
```
(補足)
* django 4.0.4 にて実装（ ver.4 以上の django の必要あり）
* サーバが立つ
* `http://127.0.0.1:8000/twemotion/` でホーム画面にアクセス
* トレンドの取得と感情分析は，15分ごとに `twemotion.views.py` にて行われる

## 実行（ショウ）
### 例
```
cd analyze
python3 getTrendingTweets.py
```
(補足)
* 実行する時点で Top10 のトレンドに関するツイートを各々200個取得
* 取得したツイートは data/currentTrend.json に保存
* 実行して取得したトレンドはcurrentTrend.jsonに同じトレンドが存在すれば、取得したツイートを同トレンド下に追加
* currentTrend.jsonは常に最後に実行した時点の Top10 のトレンドしか保存しない

## 実行（全体）
### 例
```
python3 manage.py runserver
```
(補足)
emotion.pyに以下の変更を加えないと動かなかった（加藤の環境）
* main関数の内容を`def main()`にし，main関数で`def main()`を呼び出し
* `args`がグローバル変数として機能しなかったので，他のそれぞれの関数の引数に`args`を追加
* `get\_args()`の`return parser.parse\_args()`を`return parser.parse_args(args=[])`に
* Djangoの仕様上，emotion.py含め絶対パスで指定しないといけないっぽいので，emotion.py中のパスで`../data`から始まるものを`data`から始まるように変更
