import streamlit as st
import json
import requests
import pandas as pd
from datetime import date, datetime

def json_serial(self):
    #日付型の場合には、文字列に変換します
    if isinstance(self, type(date)):
        return self.isoformat()
    #上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(self))

st.title('ゴルフトレーニング記録アプリ')
url = "http://127.0.0.1:8000/training"
res = requests.get(url)
res_training = res.json()

#ここは使用しない。
#training_dict = {}
#for training_golf in training_dict:
    #training_dict[training_golf["date"]] = training_golf["golfclub"]

df_training = pd.DataFrame(res_training)
df_training.columns = ["日付", "ゴルフクラブ", "ID"]
st.table(df_training)

with st.form(key="loc"):
    date = st.date_input("日付")
    golfclub: str = st.text_input("ゴルフクラブ")
    
    submitted = st.form_submit_button(label="送信")

    if submitted:
        url = "http://127.0.0.1:8000/training"
        data = {
        "date": date,
        "golfclub": golfclub
        }

        res = requests.post(
            url=url, 
            #data=json.dumps(data)
            data=json.dumps(data, default=json_serial)
        )

        if res.status_code == 200:
            st.success("送信成功")
            st.write(res.status_code)
            st.write(date)

        elif res.status_code != 200:
            st.write(res.status_code)

with st.form(key="put"):
    training_id = st.number_input("ID",step=1)
    date = st.date_input("日付")
    golfclub = st.text_input("ゴルフクラブ")
    
    submitted = st.form_submit_button(label="送信")

    if submitted:        
        url = "http://127.0.0.1:8000/training"
        data = {
            "training_id" : training_id,
            "date": date,
            "golfclub": golfclub
        }

        res = requests.put(
            url=url, 
            data=json.dumps(data, default=json_serial))

        if res.status_code == 200:
            st.success("更新完了")
        elif res.status_code != 200:
            st.write(res.status_code)



with st.form(key="delete"):
    #date = st.date_input("日付")
    #golfclub: str = st.text_input("ゴルフクラブ")
    training_id: int = st.number_input("ID", step=1, min_value=1)
    
    submitted = st.form_submit_button(label="削除")

    if submitted:
        # 405エラー methodが許可されていない
        #url = "http://127.0.0.1:8000/training"


        url = "http://127.0.0.1:8000/training/training_id"

        # 405エラー methodが許可されていない
        #url = "http://127.0.0.1:8000/training?training_id={training_id}"

        # 422エラー　
        #url = "http://127.0.0.1:8000/training{training_id}"
        data = {
            #"date": date,
            #"golfclub": golfclub,
            "training_id" : training_id
        }

        res = requests.delete(
            url=url, 
            #data=data
            #data=json.dumps(data)
            )

        if res.status_code == 200:
            st.success("削除成功")
            st.write(res.status_code)
        elif res.status_code != 200:
            st.write(res.status_code)


