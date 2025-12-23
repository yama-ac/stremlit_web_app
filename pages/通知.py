import streamlit as st
import time

st.title("Streamlit 標準通知デモ")

if st.button("標準通知を表示"):
    # 1. 右下にふわっと出るトースト
    st.toast("データを保存しました！", icon="💾")

    # 2. 画面内に固定されるメッセージ
    st.success("全ての処理が正常に完了しました。")

    # 3. お祝いエフェクト
    st.balloons()
