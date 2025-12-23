import streamlit as st
import pandas as pd
from datetime import datetime
import pytz  # タイムゾーンを扱うライブラリ

st.set_page_config(page_title="熊本駅 日本時刻案内", page_icon="⏰")

# --- 1. 日本時刻を取得する設定 ---
# タイムゾーンを日本(Tokyo)に指定
jst = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(jst)
current_time = now_jst.strftime("%H:%M")

st.title("⏰ 熊本駅→荒尾方面 次の発車案内")
st.write(f"現在時刻 (日本): **{current_time}**")

# --- 2. 時刻表データの準備 ---
# ※サンプルとして一部抜粋。実際にはもっと多くのデータを入れられます。
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

# --- 3. 現在時刻以降の電車を抽出 ---
# 現在の「時:分」よりも後の時刻のデータを最大3件取得
next_trains = df[df['time'] >= current_time].head(3)

# --- 4. 表示処理 ---
if not next_trains.empty:
    st.subheader("🔜 次に発車する電車")
    for _, row in next_trains.iterrows():
        # タイル状のカード形式で表示
        with st.container(border=True):
            cols = st.columns([1, 1, 1])
            cols[0].markdown(f"### {row['time']}")
            cols[1].markdown(f"\n{row['type']}")
            cols[2].markdown(f"\n{row['dest']} 行き")
else:
    st.info("本日の運行はすべて終了しました。")

# 手動更新
if st.button("時刻を更新"):
    st.rerun()

st.caption("※サーバーの場所に関わらず日本標準時(JST)で計算しています。")
