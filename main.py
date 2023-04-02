import cx_Oracle
import pandas as pd
import fuzzyAglo as fuzz
from flask import Flask,jsonify,request

app=Flask(__name__)


def getConnection():
    connection = cx_Oracle.connect('moz_aml/moz_aml@3.111.8.162:1521/xe')
    return connection

def fetchData():
    con=getConnection()
    cur = con.cursor()
    cur.execute("SELECT FIRSTNAME FROM WATCHLISTEXTERNALDATA")
    watch_list = cur.fetchall()
    cur.execute("SELECT ACC_NAME FROM CUSTOMERSHISTORY")
    customer_history = cur.fetchall()

    dict_list = []
    for name in watch_list:
        match = fuzz.get_ratio(name, customer_history, 30)
        dict_ = {}
        dict_.update({"First_Name": name})
        dict_.update({"ACC_Name": match[0]})
        dict_.update({"Score": match[1]})
        dict_list.append(dict_)

    df = pd.DataFrame(dict_list)
    matched_data = df.nlargest(n=5, columns=['Score'])
    con.commit()
    cur.close()
    con.close()
    print(matched_data)
    return matched_data

@app.route('/fuzzy',methods=['GET'])
def getData():
     db_res=fetchData()
     items=db_res.values.tolist()
     data = {
         "statusCode":200,
         "msg": "SUCCESS",
         "data":items
     }
     return jsonify(data)

@app.route('/',methods=['GET'])
def hello_world():
    return "Hello World"


if __name__=="__main__":
    app.run(debug=True,port=8000)














#
# try:
#     con = cx_Oracle.connect('moz_aml/moz_aml@3.111.8.162:1521/xe')
# except cx_Oracle.DatabaseError as er:
#     print('There is an error in the Oracle database:', er)
# else:
#     try:
#         cur = con.cursor()
#         cur.execute("SELECT FIRSTNAME FROM WATCHLISTEXTERNALDATA")
#         watch_list=cur.fetchall()
#         cur.execute("SELECT ACC_NAME FROM CUSTOMERSHISTORY")
#         customer_history=cur.fetchall()
#
#         dict_list = []
#         for name in watch_list:
#             match = fuzz.get_ratio(name, customer_history, 30)
#             dict_ = {}
#             dict_.update({"First_Name": name})
#             dict_.update({"ACC_Name": match[0]})
#             dict_.update({"Score": match[1]})
#             dict_list.append(dict_)
#
#         df = pd.DataFrame(dict_list)
#         matched_data = df.nlargest(n=5, columns=['Score'])
#         print(matched_data)
#
#     except cx_Oracle.DatabaseError as er:
#         print('There is an error in the Oracle database:', er)
#     except Exception as er:
#         print('Error:' + str(er))
#     finally:
#         if cur:
#             cur.close()
# finally:
#     if con:
#         con.close()
