import mysql.connector as mydb
import json
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y/%m/%d %H:%M:%S')

def insertTrend(trend, emotion, rank):
    with mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8") as db:
        cuesor = db.cursor()
        values = "('" + d + "','" + trend + "','" + emotion + "'," + str(rank)  + "" ")"
        # print(values)
        cuesor.execute(
            "insert into tb_Trends (subbmission_date, trend, emotion, `rank`) values " + values)
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

    with open("data/outputs/processedEmotion_trend.json", "r") as analysis_json_open:
        analysis_result = json.load(analysis_json_open)


    rank = 0

    for t in analysis_result.keys():
        rank += 1

        print(analysis_result[t])

        emotion = analysis_result[t]

        print(emotion)

        # with open("data/tweets/Trends.json", "r") as Trends_json_open:
        #     Trends_inf = json.load(Trends_json_open)
        # Trends_inf = Trends_inf[0]
        # for trend in Trends_inf['trends']:
        #     if str(trend['name']==t):
        #         tweet_volume = str(trend['tweet_volume'])

        insertTrend(t, str(emotion).replace("'", ""), rank)

if __name__ == "__main__":
    main()
