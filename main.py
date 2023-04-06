
import cx_Oracle
import pandas as pd
import fuzzyAglo as fuzz
from flask import Flask,jsonify,request
import time
from sklearn.feature_extraction.text import CountVectorizer

app=Flask(__name__)


def getConnection():
    connection = cx_Oracle.connect('moz_aml/moz_aml@3.111.8.162:1521/xe')
    return connection

def fetchData():
    con=getConnection()
    cur = con.cursor()
    cur.execute("SELECT FIRSTNAME FROM WATCHLISTEXTERNALDATA")
    watch_list = cur.fetchall()
    # watch_df = pd.DataFrame(watch, columns=["FIRSTNAME"]).dropna()
    # watch_list =watch_df.values.tolist()

    cur.execute("SELECT ACC_NAME FROM CUSTOMERSHISTORY")
    customer_history = cur.fetchall()
    # watch_df = pd.DataFrame(customer, columns=["ACC_NAME"]).dropna()
    # customer_history = watch_df.values.tolist()

    # X = CountVectorizer().fit_transform(watch).toarray()
    # Y=CountVectorizer().fit_transform(customer).toarray()
    #

    dict_list = []

    start=time.time()
    for name in  customer_history:
        match = fuzz.get_score(name, watch_list)
        dict_ = {}
        dict_.update({"First_Name": name[0]})
        dict_.update({"ACC_Name": match[0]})
        dict_.update({"Score": match[1]})
        dict_list.append(dict_)
    end=time.time()
    print(end-start)

    df = pd.DataFrame(dict_list)
    matched_data = df.nlargest(n=5, columns=['Score'])
    con.commit()
    cur.close()
    con.close()
    return matched_data

@app.route('/fuzzy',methods=['GET'])
def getData():
     db_res=fetchData()
     print(db_res)

     data = {
         "statusCode":200,
         "msg": "SUCCESS"
     }
     return jsonify(data)

@app.route('/',methods=['GET'])
def hello_world():
    return "Hello World"


if __name__=="__main__":
    app.run(debug=True,port=5000)
