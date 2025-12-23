# API
# 9c5817265dcfbbb89aedf479ba8f1c4a


import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 設定 ---
API_KEY = "9c5817265dcfbbb89aedf479ba8f1c4a"
DEFAULT_CITY = "Osaka,jp"

st.set_page_config(page_title="Weather App Design", layout="centered")

# 自動更新（10秒）
st_autorefresh(interval=10000, key="datarefresh")

# --- 画像のUIを再現するカスタムCSS ---
st.markdown("""
    <style>
    /* 全体の背景色（ダーク） */
    .stApp {
        background-color: #121212;
        color: white;
    }

    /* 共通カードデザイン */
    .card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
    }

    /* 上部の日別リスト */
    .day-box {
        text-align: center;
        padding: 10px;
        border-radius: 20px;
        background: #2a2a2a;
        min-width: 60px;
    }
    .day-box-selected {
        border: 2px solid #ffffff;
        background: #333333;
    }

    /* 巨大な気温表示 */
    .main-temp {
        font-size: 80px;
        font-weight: 200;
        margin: 0;
    }

    /* 1時間ごとのボックス */
    .hour-box {
        text-align: center;
        font-size: 0.8rem;
        color: #aaaaaa;
    }

    /* 下部の詳細カード（降水量・風） */
    .detail-card {
        background-color: #1e1e1e;
        padding: 25px;
        border-radius: 25px;
        height: 180px;
    }
    </style>
""", unsafe_allow_html=True)

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
    return requests.get(url).json()

# --- UI構築 ---
data = get_weather(DEFAULT_CITY)

if data.get("cod") == "200":
    now = datetime.now()
    current = data['list'][0]

    # 1. ヘッダー（10日間の天気予報風）
    st.markdown("### ← 10 日間の天気予報")
    day_cols = st.columns(6)
    for i in range(6):
        item = data['list'][i*8] # 24時間おきのデータ
        dt = datetime.fromtimestamp(item['dt'])
        with day_cols[i]:
            # 今日を選択中風にする
            cls = "day-box-selected" if i == 0 else "day-box"
            st.markdown(f"""
                <div class="{cls}">
                    <div style="font-size:0.7rem;">{item['main']['temp_max']:.0f}°</div>
                    <div style="font-size:0.7rem; color:#888;">{item['main']['temp_min']:.0f}°</div>
                    <img src="http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png" width="30">
                    <div style="font-size:0.6rem;">{dt.strftime('%a')}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. メイン気温エリア
    st.write(now.strftime("%m月%d日"))
    st.subheader("大阪市淀川区")

    col_main1, col_main2 = st.columns([2, 1])
    with col_main1:
        st.markdown(f'<p class="main-temp">{current["main"]["temp"]:.0f}°<span style="font-size:40px;">{current["main"]["temp_min"]:.0f}°</span></p>', unsafe_allow_html=True)
        st.markdown(f'<h3>{current["weather"][0]["description"]}</h3>', unsafe_allow_html=True)
    with col_main2:
        icon_id = current['weather'][0]['icon']
        st.image(f"http://openweathermap.org/img/wn/{icon_id}@4x.png", width=150)

    # 3. 1時間ごとの天気予報
    with st.container():
        st.markdown('<div class="card">🕒 1時間ごとの天気予報', unsafe_allow_html=True)
        h_cols = st.columns(8)
        for i in range(8):
            item = data['list'][i]
            with h_cols[i]:
                st.markdown(f"""
                    <div class="hour-box">
                        <div>{item['main']['temp']:.0f}°</div>
                        <img src="http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png" width="30">
                        <div>{datetime.fromtimestamp(item['dt']).strftime('%H:%00')}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. 下部詳細（降水量・風）
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        rain = current.get('rain', {'1h': 0}).get('1h', 0)
        st.markdown(f"""
            <div class="detail-card">
                <p style="color:#aaa;">☔ 降水量</p>
                <p style="font-size:2.5rem; margin:0;">{rain} <span style="font-size:1.2rem;">mm</span></p>
                <p style="font-size:0.8rem; color:#888; margin-top:10px;">一日の総雨量</p>
            </div>
        """, unsafe_allow_html=True)
    with col_inf2:
        wind = current['wind']['speed']
        st.markdown(f"""
            <div class="detail-card">
                <p style="color:#aaa;">🍃 風</p>
                <p style="font-size:2.5rem; margin:0;">{wind} <span style="font-size:1.2rem;">m/s</span></p>
                <p style="font-size:0.8rem; color:#888; margin-top:10px;">北東の風</p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("データの取得に失敗しました。APIキーを確認してください。")
