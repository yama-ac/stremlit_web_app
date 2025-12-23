import streamlit as st
import time

st.title("タイマー通知アプリ")
st.write("下のボタンを押すと、10秒後に通知が届きます。")

if st.button('10秒タイマーを開始'):
    # プログレスバー（進行状況）を表示して、視覚的に分かりやすくします
    progress_text = "10秒後に通知します..."
    my_bar = st.progress(0, text=progress_text)

    # 10秒間待機（1秒ごとにバーを更新）
    for percent_complete in range(100):
        time.sleep(0.1)  # 0.1秒 × 100回 = 10秒
        my_bar.progress(percent_complete + 1, text=progress_text)

    # プログレスバーを消去
    my_bar.empty()

    # 通知（トースト）を表示
    st.toast('10秒経過しました！', icon='⏰')

    # 画面上にも完了メッセージを表示
    st.success('時間です！通知を送りました。')
