import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="熊本駅 リアルタイム案内", page_icon="⏰")

st.title("⏰ 熊本駅→荒尾方面 次の発車案内")

# 1. 時刻表データの準備（本来はここを外部URLのCSVなどから読み込むと管理が楽です）
# 例: pd.read_csv("https://example.com/kumamoto_timetable.csv")
raw_data = [
    {"time": "06:01", "type": "普通", "dest": "銀水"},
    {"time": "06:35", "type": "普通", "dest": "鳥栖"},
    {"time": "07:12", "type": "区間快速", "dest": "門司港"},
    {"time": "07:45", "type": "普通", "dest": "荒尾"},
    {"time": "08:15", "type": "普通", "dest": "鳥栖"},
    {"time": "18:30", "type": "普通", "dest": "鳥栖"},
    {"time": "19:15", "type": "快速", "dest": "荒尾"},
    {"time": "20:05", "type": "普通", "dest": "鳥栖"},
    {"time": "23:50", "type": "最終", "dest": "荒尾"},
]

df = pd.DataFrame(raw_data)

# 2. 現在時刻を取得
now = datetime.now().strftime("%H:%M")
st.write(f"現在の時刻: **{now}**")

# 3. 「現在時刻以降」の電車をフィルタリング
# 文字列比較で「今の時間よりも後ろの時間」を探します
next_trains = df[df['time'] >= now].head(3)

# 4. 表示
if not next_trains.empty:
    st.subheader("🔜 次に発車する電車（直近3本）")

    # 見た目を整える
    for index, row in next_trains.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2])
            col1.metric("発車時刻", row['time'])
            col2.write(f"【{row['type']}】")
            col3.write(f"{row['dest']} 行き")
            st.divider()
else:
    st.info("本日の運行はすべて終了しました。")

# 5. 手動更新ボタン
if st.button("最新の情報に更新"):
    st.rerun()
