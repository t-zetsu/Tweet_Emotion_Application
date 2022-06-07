# git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
# cd mecab-ipadic-neologd
# /work/mecab-ipadic-neologd/libexec/install-mecab-ipadic-neologd.sh を編集76line sudoを消す
# ./bin/install-mecab-ipadic-neologd -n
# echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
# ./bin/install-mecab-ipadic-neologd -h

python3 emotion_analysis/ml_ask.py