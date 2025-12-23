# API
# 9c5817265dcfbbb89aedf479ba8f1c4a

import streamlit as st
import requests
from datetime import datetime

# --- 設定 ---
API_KEY = "9c5817265dcfbbb89aedf479ba8f1c4a"
CITY = "Osaka,jp"
URL_CURRENT = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ja"
URL_FORECAST = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=ja"

st.set_page_config(page_title="Osaka Weather Pro", layout="centered")

# スタイル
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_weather(url):
    res = requests.get(url)
    return res.json()

try:
    # --- 1. 現在の天気 ---
    current_data = get_weather(URL_CURRENT)
    if current_data.get("cod") != 200:
        st.error(f"エラー: {current_data.get('message')}")
    else:
        main = current_data['main']
        weather = current_data['weather'][0]
        icon_id = weather['icon'] # OWM独自のアイコンID
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@4x.png"

        st.title(f"🏙️ {current_data['name']} の天気")

        # メイン表示
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(icon_url)
        with col2:
            st.metric("現在の気温", f"{main['temp']} ℃")
            st.write(f"**天気:** {weather['description']}")
            st.write(f"**湿度:** {main['humidity']}% / **体感:** {main['feels_like']}℃")

        st.divider()

        # --- 2. 5日間予報（3時間おき） ---
        st.subheader("🗓️ 5日間の予報（3時間ごと）")
        forecast_data = get_weather(URL_FORECAST)

        # 最初の8つ（24時間分）をピックアップして表示
        forecast_list = forecast_data['list'][:8]
        cols = st.columns(4)

        for i, item in enumerate(forecast_list):
            with cols[i % 4]:
                dt = datetime.fromtimestamp(item['dt']).strftime('%m/%d %H:%M')
                f_icon = item['weather'][0]['icon']
                st.markdown(f"""
                    <div class="metric-card">
                        <p style="font-size:0.8rem;">{dt}</p>
                        <img src="http://openweathermap.org/img/wn/{f_icon}.png" width="50">
                        <p style="font-weight:bold; margin:0;">{item['main']['temp']}℃</p>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")

except Exception as e:
    st.warning("APIキーが有効になるまで時間がかかる場合があります（401エラーなど）。")
