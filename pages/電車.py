import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="熊本駅 発車案内", page_icon="⏰")

# --- 1. 日本時刻を取得 ---
jst = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(jst)
current_time = now_jst.strftime("%H:%M")

st.title("⏰ 熊本駅→荒尾方面 発車案内")
st.write(f"現在時刻: **{current_time}**")

# --- 2. 時刻表データの準備 (昇順で並んでいることが前提) ---
raw_data = [
    {"time": "06:01", "type": "普通", "dest": "銀水"},
    {"time": "06:35", "type": "普通", "dest": "鳥栖"},
    {"time": "07:12", "type": "区間快速", "dest": "門司港"},
    {"time": "07:45", "type": "普通", "dest": "荒尾"},
    {"time": "18:30", "type": "普通", "dest": "鳥栖"},
    {"time": "21:15", "type": "快速", "dest": "荒尾"},
    {"time": "22:05", "type": "普通", "dest": "鳥栖"},
    {"time": "23:50", "type": "最終", "dest": "荒尾"},
]
df = pd.DataFrame(raw_data)

# --- 3. 表示する電車の選別 ---
# 現在時刻以降の電車を探す
next_trains = df[df['time'] >= current_time].head(3)

is_tomorrow = False
# もし現在時刻以降に電車がない場合、明日の始発を表示
if next_trains.empty:
    next_trains = df.head(1) # 時刻表の1番上を取得
    is_tomorrow = True

# --- 4. 表示処理 ---
if is_tomorrow:
    st.warning("🌙 本日の運行は終了しました。明日の始発をご案内します。")
else:
    st.subheader("🔜 次に発車する電車")

for _, row in next_trains.iterrows():
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1, 1])
        # 明日の場合は日付を表示
        label = "発車時刻" if not is_tomorrow else "明日始発"
        col1.metric(label, row['time'])
        col2.markdown(f"\n**{row['type']}**")
        col3.markdown(f"\n{row['dest']} 行き")

# 手動更新ボタン
if st.button("情報を更新"):
    st.rerun()

st.caption("※この案内は登録された時刻表に基づいています。最新の遅延情報は別途確認してください。")
