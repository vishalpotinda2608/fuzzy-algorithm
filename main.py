
import cx_Oracle
import pandas as pd
import fuzzyAglo as fuzz
from flask import Flask,jsonify,request
import time

app=Flask(__name__)


def getConnection():
    connection = cx_Oracle.connect('moz_aml/moz_aml@3.111.8.162:1521/xe')
    return connection

def fetchData():
    start=time.time()
    con=getConnection()
    cur = con.cursor()

    cur.execute("SELECT ACC_NAME FROM CUSTOMERSHISTORY")
    customer = cur.fetchall()
    watch_df = pd.DataFrame(customer, columns=["ACC_NAME"]).dropna()
    customer_history = watch_df.values.tolist()

    cur.execute("SELECT FIRSTNAME FROM WATCHLISTEXTERNALDATA")
    watch_list = cur.fetchall()

    end = time.time()
    print("db time:", end - start)
    print(len(customer_history))
    print(len(watch_list))

    dict_list = []

    start=time.time()
    for name in  customer_history:
        match = fuzz.get_score(name, watch_list)
        # if match[1] > 0:
        #     save_watcheslist_data(match[0],match[1])
        # else:
        #     pass

        dict_ = {}
        dict_.update({"ACC_Name": name[0]})
        dict_.update({"First_Name": match[0]})
        dict_.update({"Similarity": match[1]})
        dict_list.append(dict_)
    end=time.time()
    print("cosine time:",end-start)

    df = pd.DataFrame(dict_list)
    matched_data = df.nlargest(n=5, columns=['Similarity'])
    con.commit()
    cur.close()
    con.close()
    return matched_data


def save_watcheslist_data():
    con=getConnection()
    cur=con.cursor()
    cur.execute("INSERT INTO WATCHLISTMATCHDETAILS(ID,CUSTTYPE,TYPE,CUSTID,CUSTHISTORYID,MATCHKEYS,WATCHLISTMATCHKEYS,SCORE,TOTALSCORE,PERCENTAGESCORE,MATCHVALUES,MATCHWATCHLISTVALUES,WATCHLISTID,ACCID) VALUES ('8329241021','11','EXTERNAL','15760','NA','ACC_NAME','TITLE,FIRSTNAME,MIDDLENAME,LASTNAME,DATATYPE','99.99','80','80','Vishal','vishal the fraduer','26088','PT877393907')")
    watch_details = cur.fetchall()
    print(watch_details)

@app.route('/fuzzy',methods=['GET'])
def getData():
     matched_data_df=fetchData()
     print(matched_data_df)
     matched_list=matched_data_df.values.tolist()
     result=[]
     for i in range(len(matched_list)):
         match_dic={}
         match_dic.update({"ACC_Name":matched_list[i][0]})
         match_dic.update({"FIRSTNAME":matched_list[i][1]})
         match_dic.update({"Similarity":matched_list[i][2]})
         result.append(match_dic)

     data = {
         "statusCode":200,
         "msg": "SUCCESS",
         "data":result
     }
     return jsonify(data)

@app.route('/',methods=['GET'])
def hello_world():
    return "Hello World"



if __name__=="__main__":
    app.run(debug=True,port=5000)
