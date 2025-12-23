# API
# 9c5817265dcfbbb89aedf479ba8f1c4a


import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from streamlit_autorefresh import st_autorefresh

# --- 設定 ---
API_KEY = "9c5817265dcfbbb89aedf479ba8f1c4a"
DEFAULT_CITY = "Osaka"
JST = timezone(timedelta(hours=+9), 'JST')

# layout="wide" でStreamlit側の制限を解除
st.set_page_config(page_title="Weather Dashboard Pro", layout="wide")

st_autorefresh(interval=5000, key="datarefresh")

# --- スタイル設定 (フルワイド最適化) ---
st.markdown("""
    <style>
    /* コンテンツの最大幅制限を解除し、左右の余白を最小化 */
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1rem !important;
    }

    /* 時計のデザイン */
    .clock-container { text-align: center; padding: 10px; margin-bottom: 10px; }
    .clock-display { font-size: 4rem !important; font-weight: 900; color: #2563eb; margin: 0; }
    .date-display { font-size: 1.5rem; color: #1e293b; font-weight: bold; }

    /* メインカードも横に広がるよう調整 */
    .main-card {
        background-color: #0f172a; color: white; padding: 30px; border-radius: 25px;
        text-align: center; margin-bottom: 30px; border: 4px solid #2563eb;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        width: 100%;
    }

    /* 横スクロールコンテナ（PCでもフルに活用） */
    .scroll-container {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding: 10px 5px 25px 5px;
        -webkit-overflow-scrolling: touch;
    }

    /* スクロールバーを見やすく */
    .scroll-container::-webkit-scrollbar { height: 10px; }
    .scroll-container::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
    .scroll-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    .scroll-container::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* 予報ボックスのデザイン */
    .forecast-box {
        flex: 0 0 140px; /* PCで見栄えが良いように少し大きめに設定 */
        background-color: white; padding: 20px; border-radius: 20px;
        text-align: center; border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .forecast-box:hover { transform: translateY(-5px); }

    .time-label-large { font-size: 1.6rem !important; font-weight: 800; color: #1e293b; }
    .temp-label-red { font-size: 1.5rem; font-weight: bold; color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
    try:
        res = requests.get(url).json()
        return res
    except: return None

# --- UI部分 ---
now = datetime.now(JST)

st.markdown(f"""
    <div class="clock-container">
        <p class="date-display">{now.strftime("%Y年%m月%d日 (%a)")}</p>
        <p class="clock-display">{now.strftime("%H:%M:%S")}</p>
    </div>
""", unsafe_allow_html=True)

city_input = st.sidebar.text_input("表示地域を検索", value=DEFAULT_CITY)

if city_input:
    data = get_weather_data(city_input)
    if not data or data.get("cod") != "200":
        st.error(f"都市 '{city_input}' のデータが見つかりませんでした。")
    else:
        forecast_list = data['list']
        current_data = min(forecast_list, key=lambda x: abs(datetime.fromtimestamp(x['dt'], JST) - now))
        icon_url = f"http://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}@4x.png"

        # メインカード（フルワイド表示）
        st.markdown(f"""
            <div class="main-card">
                <h2 style="margin:0; color: #60a5fa; letter-spacing: 3px; font-size: 1.8rem;">{data['city']['name'].upper()}</h2>
                <img src="{icon_url}" style="width:140px;">
                <h1 style="font-size: 5rem; margin: 0;">{current_data['main']['temp']}℃</h1>
                <p style="font-size: 2rem; margin: 0; font-weight: bold;">{current_data['weather'][0]['description']}</p>
                <div style="display: flex; justify-content: center; gap: 40px; margin-top: 20px; font-size: 1.2rem; opacity: 0.9;">
                    <span>💧 湿度: {current_data['main']['humidity']}%</span>
                    <span>💨 風速: {current_data['wind']['speed']}m/s</span>
                    <span>🌡️ 体感: {current_data['main']['feels_like']}℃</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 3時間ごとの詳細予報
        st.subheader("⏱️ 3時間ごとの詳細予報")
        timeline_html = '<div class="scroll-container">'
        # PCサイトではより多くの予報（15件分など）を表示
        for item in forecast_list[:15]:
            t_obj = datetime.fromtimestamp(item['dt'], JST)
            icon = item['weather'][0]['icon']
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            timeline_html += f"""
                <div class="forecast-box">
                    <div class="time-label-large">{t_obj.strftime('%H:%M')}</div>
                    <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="70">
                    <div class="temp-label-red">{temp}℃</div>
                    <div style="font-size:0.9rem; color:#1e293b; font-weight:bold; margin-top:5px;">{desc}</div>
                </div>"""
        timeline_html += '</div>'
        st.markdown(timeline_html, unsafe_allow_html=True)

        # 週間予報
        st.subheader("🗓️ 週間予報 (5日間)")
        daily_forecasts = []
        seen_days = set()
        for item in forecast_list:
            dt_obj = datetime.fromtimestamp(item['dt'], JST)
            day_str = dt_obj.strftime('%Y-%m-%d')
            if day_str != now.strftime('%Y-%m-%d') and day_str not in seen_days:
                if dt_obj.hour >= 12:
                    daily_forecasts.append(item)
                    seen_days.add(day_str)

        week_html = '<div class="scroll-container">'
        for day_data in daily_forecasts:
            d_obj = datetime.fromtimestamp(day_data['dt'], JST)
            icon = day_data['weather'][0]['icon']
            temp = day_data['main']['temp']
            desc = day_data['weather'][0]['description']
            week_html += f"""
                <div class="forecast-box">
                    <div class="time-label-large" style="font-size: 1.4rem !important;">{d_obj.strftime('%m/%d')}</div>
                    <div style="color: #1e293b; font-weight: bold; font-size:1rem;">({d_obj.strftime('%a')})</div>
                    <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="70">
                    <div class="temp-label-red">{temp}℃</div>
                    <div style="font-size:0.9rem; color:#1e293b; font-weight:bold; margin-top:5px;">{desc}</div>
                </div>"""
        week_html += '</div>'
        st.markdown(week_html, unsafe_allow_html=True)
else:
    st.info("左側のサイドバーに都市名を入力してください。")
