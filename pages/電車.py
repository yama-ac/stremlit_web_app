import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="熊本→荒尾 運行案内", page_icon="🚃")

# --- 1. 日本時刻を取得 ---
jst = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(jst)
current_time = now_jst.strftime("%H:%M")

st.title("🚃 熊本駅 → 荒尾駅 運行案内")
st.write(f"現在時刻: **{current_time}**")

# --- 2. 時刻表データの準備 (所要時間を追加) ---
# duration: 熊本から荒尾までの所要時間(分)
raw_data = [
    {"time": "06:01", "type": "普通", "dest": "銀水", "duration": 52},
    {"time": "06:35", "type": "普通", "dest": "鳥栖", "duration": 50},
    {"time": "07:12", "type": "区間快速", "dest": "門司港", "duration": 42},
    {"time": "07:45", "type": "普通", "dest": "荒尾", "duration": 48},
    {"time": "18:30", "type": "普通", "dest": "鳥栖", "duration": 51},
    {"time": "19:15", "type": "快速", "dest": "荒尾", "duration": 38},
    {"time": "22:05", "type": "普通", "dest": "鳥栖", "duration": 49},
    {"time": "23:50", "type": "最終", "dest": "荒尾", "duration": 48},
]
df = pd.DataFrame(raw_data)

# --- 3. 到着時刻を計算する関数 ---
def calculate_arrival(departure_str, duration_min):
    dep_time = datetime.strptime(departure_str, "%H:%M")
    from datetime import timedelta
    arrival_time = dep_time + timedelta(minutes=duration_min)
    return arrival_time.strftime("%H:%M")

# --- 4. 表示する電車の選別 ---
next_trains = df[df['time'] >= current_time].head(3)
is_tomorrow = False

if next_trains.empty:
    next_trains = df.head(1)
    is_tomorrow = True

# --- 5. メイン表示エリア ---
if is_tomorrow:
    st.warning("🌙 本日の運行は終了しました。明日の始発をご案内します。")
else:
    st.subheader("🔜 次に発車する電車")

for _, row in next_trains.iterrows():
    arrival_time = calculate_arrival(row['time'], row['duration'])

    with st.container(border=True):
        # 4つのカラムで情報を整理
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])

        c1.metric("発車", row['time'])
        c2.write(f"**{row['type']}**")
        c3.write(f"{row['dest']}行")

        # 運行時間の詳細
        with c4:
            st.write(f"⏱️ 所要時間: **{row['duration']}分**")
            st.caption(f"🏁 荒尾駅 {arrival_time} 着予定")

# --- 6. 路線図のイメージ（視覚的な補助） ---
st.divider()
st.info("💡 熊本駅〜荒尾駅間は、快速を利用すると約40分、普通列車で約50分です。")

# 更新ボタン
if st.button("最新の情報に更新"):
    st.rerun()
