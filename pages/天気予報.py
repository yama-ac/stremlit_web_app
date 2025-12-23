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

st.set_page_config(page_title="Weather Dashboard Pro", layout="wide")

st_autorefresh(interval=5000, key="datarefresh")

# --- スタイル設定 (PC・タブレット向けの最適化) ---
st.markdown("""
    <style>
    /* コンテンツ全体の最大幅を制限して中央寄せ */
    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }

    /* 時計とメインカードのデザイン */
    .clock-container { text-align: center; padding: 10px; margin-bottom: 20px; }
    .clock-display { font-size: 3.5rem !important; font-weight: 900; color: #2563eb; margin: 0; }
    .date-display { font-size: 1.3rem; color: #1e293b; font-weight: bold; }

    .main-card {
        background-color: #0f172a; color: white; padding: 30px; border-radius: 25px;
        text-align: center; margin-bottom: 30px; border: 4px solid #2563eb;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    /* 横スクロールコンテナ */
    .scroll-container {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding: 10px 5px 20px 5px;
        -webkit-overflow-scrolling: touch;
    }

    /* スクロールバーのデザイン（PCで見えやすく） */
    .scroll-container::-webkit-scrollbar { height: 8px; }
    .scroll-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

    /* 予報ボックス */
    .forecast-box {
        flex: 0 0 120px; /* PC向けに少し幅を広げた */
        background-color: white; padding: 15px; border-radius: 18px;
        text-align: center; border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    .time-label-large { font-size: 1.5rem !important; font-weight: 800; color: #1e293b; }
    .temp-label-red { font-size: 1.4rem; font-weight: bold; color: #ef4444; }
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

        # メインカード
        st.markdown(f"""
            <div class="main-card">
                <h2 style="margin:0; color: #60a5fa; letter-spacing: 2px; font-size: 1.5rem;">{data['city']['name'].upper()}</h2>
                <img src="{icon_url}" style="width:120px;">
                <h1 style="font-size: 4.5rem; margin: 0;">{current_data['main']['temp']}℃</h1>
                <p style="font-size: 1.8rem; margin: 0; font-weight: bold;">{current_data['weather'][0]['description']}</p>
                <p style="font-size: 1rem; opacity: 0.8; margin-top: 10px;">
                    湿度: {current_data['main']['humidity']}% / 風速: {current_data['wind']['speed']}m/s
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 3時間ごとの詳細予報
        st.subheader("⏱️ 3時間ごとの詳細予報")
        timeline_html = '<div class="scroll-container">'
        for item in forecast_list[:12]:
            t_obj = datetime.fromtimestamp(item['dt'], JST)
            icon = item['weather'][0]['icon']
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            timeline_html += f"""
                <div class="forecast-box">
                    <div class="time-label-large">{t_obj.strftime('%H:%M')}</div>
                    <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="60">
                    <div class="temp-label-red">{temp}℃</div>
                    <div style="font-size:0.8rem; color:#1e293b; font-weight:bold;">{desc}</div>
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
                    <div class="time-label-large" style="font-size: 1.3rem !important;">{d_obj.strftime('%m/%d')}</div>
                    <div style="color: #1e293b; font-weight: bold; font-size:0.9rem;">({d_obj.strftime('%a')})</div>
                    <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="60">
                    <div class="temp-label-red">{temp}℃</div>
                    <div style="font-size:0.8rem; color:#1e293b; font-weight:bold;">{desc}</div>
                </div>"""
        week_html += '</div>'
        st.markdown(week_html, unsafe_allow_html=True)
else:
    st.info("左側のサイドバーに都市名を入力してください。")
