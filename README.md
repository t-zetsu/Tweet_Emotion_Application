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
docker run -it -d --ipc=host -v [WORK_DIR] --name [CONTAINER_NAME] [IMAGE_NAME] /bin/bash
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
* data内にある最新(?)のjsonファイルのツイートを分析
* analyze内にresult.jsonが生成される

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