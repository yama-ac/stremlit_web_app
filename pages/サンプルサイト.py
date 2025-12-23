# API
# 9c5817265dcfbbb89aedf479ba8f1c4a

import streamlit as st
import requests
from datetime import datetime

# --- 設定 ---
API_KEY = "9c5817265dcfbbb89aedf479ba8f1c4a"  # 取得したAPIキーに書き換えてください

# ページ設定
st.set_page_config(page_title="Weather Dashboard", layout="centered")

# --- スタイル設定 ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .current-box {
        background-color: #1e293b;
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .forecast-card {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- データ取得関数 ---
def get_weather_data(city_name):
    # 現在の天気
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ja"
    # 5日間予報
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric&lang=ja"

    curr_res = requests.get(current_url).json()
    fore_res = requests.get(forecast_url).json()

    return curr_res, fore_res

# --- UI部分 ---
st.title("🌡️ お天気検索ダッシュボード")

# 地域入力欄 (デフォルトを "Osaka" に設定)
city_input = st.text_input("都市名を入力してください（例: Tokyo, Nagoya, London）", value="Osaka")

if city_input:
    curr_data, fore_data = get_weather_data(city_input)

    # 都市が見つからない場合の処理
    if curr_data.get("cod") != 200:
        st.error(f"都市 '{city_input}' が見つかりませんでした。綴りを確認してください。")
    else:
        # 1. 現在の天気表示
        st.subheader(f"📍 {curr_data['name']} の現在の天気")

        main = curr_data['main']
        weather = curr_data['weather'][0]
        icon_id = weather['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"

        st.markdown(f"""
            <div class="current-box">
                <img src="{icon_url}" style="width:120px;">
                <h1 style="margin:0; font-size: 3rem; color: white;">{main['temp']}℃</h1>
                <p style="font-size: 1.5rem; opacity: 0.9;">{weather['description']}</p>
                <p style="font-size: 0.9rem; opacity: 0.7;">湿度: {main['humidity']}% / 体感: {main['feels_like']}℃</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. 5日間予報（3時間おき）
        st.subheader("🕒 今後の予報 (3時間ごと)")

        # 予報データを横並びにする
        forecast_list = fore_data['list'][:8] # 直近24時間分
        cols = st.columns(4)

        for i, item in enumerate(forecast_list):
            with cols[i % 4]:
                dt = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                f_icon = item['weather'][0]['icon']
                f_temp = item['main']['temp']

                st.markdown(f"""
                    <div class="forecast-card">
                        <div style="color: #64748b; font-size: 0.8rem; font-weight: bold;">{dt}</div>
                        <img src="http://openweathermap.org/img/wn/{f_icon}.png" width="50">
                        <div style="font-size: 1.1rem; font-weight: bold; color: #1e293b;">{f_temp}℃</div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("") # スペース用

else:
    st.info("都市名を入力してエンターキーを押してください。")
