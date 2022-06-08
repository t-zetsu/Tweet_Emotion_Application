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

## 実行
### 例
```
cd example
bash run.sh
```
