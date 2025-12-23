# API
# 9c5817265dcfbbb89aedf479ba8f1c4a


import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 設定 ---
API_KEY = "9c5817265dcfbbb89aedf479ba8f1c4a"
DEFAULT_CITY = "Osaka"

st.set_page_config(page_title="Weather Dashboard Pro", layout="wide")

# --- 自動更新の設定 (5秒ごとにリフレッシュ) ---
st_autorefresh(interval=5000, key="datarefresh")

# --- スタイル設定 ---
st.markdown("""
    <style>
    /* 現在時刻の時計表示 */
    .clock-container {
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e2e8f0;
    }
    .clock-display {
        font-size: 4rem !important; /* さらに大きく */
        font-weight: 900;
        color: #2563eb; /* 鮮やかなブルーで見やすく */
        margin: 0;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .date-display {
        font-size: 1.5rem;
        color: #1e293b; /* 濃いネイビー */
        font-weight: bold;
    }

    /* 現在の天気のメインカード */
    .main-card {
        background-color: #0f172a; color: white; padding: 25px; border-radius: 20px;
        text-align: center; margin-bottom: 30px; border: 4px solid #2563eb;
    }

    /* 時刻ラベル (3時間ごと・週間共通) */
    .time-label-large {
        font-size: 2rem !important;
        font-weight: 800;
        color: #1e293b; /* 視認性の高い濃い色 */
    }

    /* 予報ボックス */
    .forecast-box {
        background-color: white; padding: 15px; border-radius: 15px;
        text-align: center; border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    /* 気温ラベル */
    .temp-label-red {
        font-size: 1.5rem; font-weight: bold; color: #ef4444; /* 鮮やかな赤 */
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
    try:
        res = requests.get(url).json()
        return res
    except:
        return None

# --- UI部分 ---
# 現在時刻の表示セクション
now = datetime.now()
st.markdown(f"""
    <div class="clock-container">
        <p class="date-display">{now.strftime("%Y年%m月%d日 (%a)")}</p>
        <p class="clock-display">{now.strftime("%H:%M:%S")}</p>
    </div>
""", unsafe_allow_html=True)

# サイドバー
city_input = st.sidebar.text_input("表示地域を検索", value=DEFAULT_CITY)

if city_input:
    data = get_weather_data(city_input)

    if not data or data.get("cod") != "200":
        st.error(f"都市 '{city_input}' のデータが見つかりませんでした。")
    else:
        forecast_list = data['list']

        # 1. 今の天気
        current_data = min(forecast_list, key=lambda x: abs(datetime.fromtimestamp(x['dt']) - now))

        icon_url = f"http://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}@4x.png"
        st.markdown(f"""
            <div class="main-card">
                <h2 style="margin:0; color: #60a5fa; letter-spacing: 2px;">{data['city']['name'].upper()}</h2>
                <img src="{icon_url}" style="width:130px;">
                <h1 style="font-size: 4.5rem; margin: 0;">{current_data['main']['temp']}℃</h1>
                <p style="font-size: 1.8rem; margin: 0; font-weight: bold;">{current_data['weather'][0]['description']}</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. 3時間ごとのタイムライン
        st.subheader("⏱️ 3時間ごとの詳細予報")
        timeline_cols = st.columns(8)
        for i, item in enumerate(forecast_list[:8]):
            with timeline_cols[i]:
                t_obj = datetime.fromtimestamp(item['dt'])
                st.markdown(f"""
                    <div class="forecast-box">
                        <div class="time-label-large">{t_obj.strftime('%H:%M')}</div>
                        <img src="http://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png" width="60">
                        <div class="temp-label-red">{item['main']['temp']}℃</div>
                        <div style="font-size:0.8rem; color:#1e293b; font-weight:bold;">{item['weather'][0]['description']}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. 週間予報 (文字色とデザインを3時間ごとに統一)
        st.subheader("🗓️ 週間予報 (5日間)")
        daily_forecasts = []
        seen_days = set()
        for item in forecast_list:
            dt_obj = datetime.fromtimestamp(item['dt'])
            day_str = dt_obj.strftime('%Y-%m-%d')
            if day_str != now.strftime('%Y-%m-%d') and day_str not in seen_days:
                if dt_obj.hour >= 12:
                    daily_forecasts.append(item)
                    seen_days.add(day_str)

        week_cols = st.columns(len(daily_forecasts))
        for i, day_data in enumerate(daily_forecasts):
            with week_cols[i]:
                d_obj = datetime.fromtimestamp(day_data['dt'])
                st.markdown(f"""
                    <div class="forecast-box">
                        <div class="time-label-large" style="font-size: 1.5rem !important;">{d_obj.strftime('%m/%d')}</div>
                        <div style="color: #1e293b; font-weight: bold; margin-bottom: 5px;">({d_obj.strftime('%a')})</div>
                        <img src="http://openweathermap.org/img/wn/{day_data['weather'][0]['icon']}@2x.png" width="60">
                        <div class="temp-label-red">{day_data['main']['temp']}℃</div>
                        <div style="font-size:0.8rem; color:#1e293b; font-weight:bold;">{day_data['weather'][0]['description']}</div>
                    </div>
                """, unsafe_allow_html=True)

else:
    st.info("左側のサイドバーに都市名を入力してください。")
