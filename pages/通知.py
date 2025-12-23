import streamlit as st
import time

st.title("通知デモアプリ")

if st.button('処理を開始'):
    with st.spinner('計算中...'):
        time.sleep(2) # 重い処理の代わり

    # 標準のトースト通知
    st.toast('処理が完了しました！', icon='✅')


import streamlit as st
from streamlit_push_notifications import send_push

st.title("プッシュ通知テスト")

if st.button("ブラウザ通知を送る"):
    # ブラウザの通知許可が求められ、許可されると通知が飛びます
    send_push(
        title="重要なお知らせ",
        body="タスクが完了しました！ブラウザを確認してください。",
        icon_path="https://streamlit.io/images/brand/streamlit-mark-color.png"
    )
