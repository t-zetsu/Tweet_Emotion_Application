import mysql.connector as mydb
import json
import datetime
import ast

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
d = now.strftime('%Y/%m/%d %H:%M:%S')

def connect():
    db = mydb.connect(
            host="localhost",
            user="root",
            passwd="19971221",
            db="TDataBase",
            charset="utf8")
    return db

def process(res):
    dict = {}
    for r in res:
        date = r[2].strftime('%y/%m/%d %H:%M:%S')
        emo = ast.literal_eval(r[1])
        if r[0] not in dict:
            dict.update({r[0]:{date:[emo,{'rank':r[3]}]}})
        else : dict[r[0]].update({date:[emo,{'rank':r[3]}]})
    return dict




def createTable():
    with connect() as db:
        table = 'tb_Trends'
        cuesor = db.cursor()
        cuesor.execute(
                """
                CREATE TABLE IF NOT EXISTS `""" + table +"""` (
                `trend` varchar(255) NOT NULL,
                `emotion` varchar(1000) NOT NULL,
                `subbmission_date` timestamp NOT NULL,
                `rank` int NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """)
            


def insertTrend(trend, emotion, rank):
    createTable()
    with connect() as db:

        cuesor = db.cursor()
        values = "('" + d + "','" + trend + "','" + emotion + "'," + str(rank)  + "" ")"
        # print(values)
        cuesor.execute(
            "insert into tb_Trends (subbmission_date, trend, emotion, `rank`) values " + values)
        db.commit()

def selectTrendByTime(t1, t2): # str "YYYY-MM-DD hh:mm:ss"
    with connect() as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where subbmission_date between '" + t1 + "' AND '" + t2 + "'"
        # print(sql)
        cursor.execute(sql)
        request = cursor.fetchall()
        cursor.close()
        result = process(request)
    return result

def selectTrendByRank(rank):  # int 1~10
    with connect() as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where `rank`='" + rank  +"'"
        # print(sql)
        cursor.execute(sql)
        request = cursor.fetchall()
        cursor.close()
        result = process(request)
    return result

def selectTrendByEmo(emo):  # str 
    with connect() as db:
        cursor = db.cursor(buffered=True)
        sql = "SELECT * FROM tb_Trends where emotion like '{" + emo + "%'";
        # print(sql)
        cursor.execute(sql)
        request = cursor.fetchall()
        cursor.close()
        result = process(request)
    return result




def main():

    with open("data/outputs/processedEmotion_trend.json", "r") as analysis_json_open:
        analysis_result = json.load(analysis_json_open)


    rank = 0

    for t in analysis_result.keys():
        rank += 1

        print(analysis_result[t])

        emotion = analysis_result[t]

        list = sorted(emotion.items(), key= lambda x: x[1], reverse=True)
        emotion.clear()
        emotion.update(list)

        print(emotion)

        # with open("data/tweets/Trends.json", "r") as Trends_json_open:
        #     Trends_inf = json.load(Trends_json_open)
        # Trends_inf = Trends_inf[0]
        # for trend in Trends_inf['trends']:
        #     if str(trend['name']==t):
        #         tweet_volume = str(trend['tweet_volume'])

        insertTrend(t, str(emotion).replace("'", r"\'"), rank)

if __name__ == "__main__":
    main()
