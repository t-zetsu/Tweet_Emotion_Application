import mysql.connector as mydb
import json
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y/%m/%d %H:%M:%S')

def insertTrend(trend, emotion, rank, vol):
    with mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8") as db:
        cuesor = db.cursor()
        values = "('" + d + "','" + trend + "','" + emotion + "'," + str(rank) +  ",'" + vol + "'" ")"
        # print(values)
        cuesor.execute(
            "insert into tb_Trends (subbmission_date, trend, emotion, `rank`, vol) values " + values)
        db.commit()

def selectTrendByTime(t1, t2): # str "YYYY-MM-DD hh:mm:ss"
    with mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8") as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where subbmission_date between '" + t1 + "' AND '" + t2 + "'"
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    return result

def selectTrendByRank(rank):  # int 1~10
    with mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8") as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where `rank`='" + rank  +"'"
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    return result

def selectTrendByEmo(emo):  # str 
    with mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8") as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where emotion like '{" + emo + "%'";
        # print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    return result




def main():

    with open("data/outputs/currentEmotion.json", "r") as analysis_json_open:
        analysis_result = json.load(analysis_json_open)

    analysis_result = {key.replace(
        "#", ""): value for key, value in analysis_result.items()}

    rank = 0

    for t in analysis_result.keys():
        rank += 1
        with open("config/emotion_display.json", "r") as color_json_open:
            emotion_dic = json.load(color_json_open)
        for tweet in analysis_result[t]:
            for em in tweet["emotion"]:
                emotion_dic[em]["point"] += 100 / \
                    (len(analysis_result[t]) * len(tweet["emotion"]))
        emotion_dic.pop('None')
        point_sum = 0
        for k, v in emotion_dic.items():
            point_sum += v['point']
        for k in emotion_dic.keys():
            emotion_dic[k]['point'] *= 100 / point_sum
        for em, content in emotion_dic.items():
            content["point"] = round(content["point"], 3)  # 丸め
        emotion_dic = sorted(emotion_dic.items(
        ), key=lambda x: x[1]["point"], reverse=True)  # 感情ポイントが多い順にソート
        emotion_dic = {item[0]: item[1]
                    for item in emotion_dic if item[1]["point"] != 0}
        emotion = {}
        for em, content in emotion_dic.items():
            emotion.update({content["japanese"]: content["point"]})
        emotion = str(emotion).replace("'","")
        print(t)

        with open("data/tweets/Trends.json", "r") as Trends_json_open:
            Trends_inf = json.load(Trends_json_open)
        Trends_inf = Trends_inf[0]
        for trend in Trends_inf['trends']:
            if str(trend['name']==t):
                tweet_volume = str(trend['tweet_volume'])

        insertTrend(t, str(emotion), rank, tweet_volume)

if __name__ == "__main__":
    main()
