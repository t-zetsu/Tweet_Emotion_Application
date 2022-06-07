# Tweet_Emotion_Application
Multi Media Engineering Exercise

## 準備
形態素解析エンジンMeCabと共に使う単語分かち書き辞書[mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)のダウンロードが必要
```
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd #mecab-ipadic-neologd/libexec/install-mecab-ipadic-neologd.shの76行目のsudoを消す必要あり？
./bin/install-mecab-ipadic-neologd -n
echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
# echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
```
