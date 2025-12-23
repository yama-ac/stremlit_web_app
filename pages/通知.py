import streamlit as st
import time

st.set_page_config(page_title="通知デモ", layout="centered")

st.title("🚀 アクション完了通知")

# ボタンの作成
if st.button('データ処理を実行'):
    # 1. 処理中の状態を表示
    with st.spinner('処理しています...'):
        time.sleep(2)  # ここに実際の処理を記述します

    # 2. 右下にふわっと通知（トースト）
    st.toast('処理が正常に完了しました！', icon='✅')

    # 3. 画面の中央にしっかりメッセージを表示（任意）
    st.success('すべてのタスクが終了しました。')

    # 4. お祝いのエフェクト（必要に応じて）
    st.balloons()
