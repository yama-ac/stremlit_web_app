import streamlit as st
import requests
import pandas as pd

# ODPTのアクセストークン（自分のものに置き換えてください）
API_KEY = "YOUR_ACCESS_TOKEN_HERE"

st.title("🚃 JR鹿児島本線 リアルタイム案内 (ODPT)")

def get_odpt_data(endpoint):
    base_url = "https://api.odpt.org/api/v4/"
    url = f"{base_url}{endpoint}?acl:consumerKey={API_KEY}"

    # 例: 鹿児島本線(上り)の列車情報を取得する場合のフィルタ
    # url += "&odpt:railway=odpt.Railway:JR-Kyushu.Kagoshima"

    response = requests.get(url)
    return response.json()

if st.button('最新情報を取得'):
    with st.spinner('データを照会中...'):
        # 列車位置情報を取得
        data = get_odpt_data("odpt:Train")

        if data:
            # 取得したJSONデータを解析して表示
            # (注: JR九州のデータ構造に合わせて加工が必要です)
            st.json(data) # まずは生データを表示して中身を確認
        else:
            st.warning("現在取得できるリアルタイム情報がありません。")

st.info("※リアルタイムAPIの利用には、ODPTセンターへの申請と利用規約の遵守が必要です。")
