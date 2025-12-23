import streamlit as st
import time
import streamlit.components.v1 as components

# 1. ページ設定
st.set_page_config(page_title="通知テスト", layout="centered")

def send_notification(title, text):
    # JavaScriptのコードを安全に生成
    # JS内の { } は Pythonの f-string 内では {{ }} と書く必要があります
    js_code = f"""
    <script>
    if (Notification.permission === "granted") {{
        new Notification("{title}", {{ body: "{text}" }});
    }} else {{
        Notification.requestPermission().then(p => {{
            if (p === "granted") {{
                new Notification("{title}", {{ body: "{text}" }});
            }}
        }});
    }}
    </script>
    """
    components.html(js_code, height=0)

st.title("🔔 デスクトップ通知アプリ")

if st.button("10秒タイマーを開始"):
    st.info("タイマーを開始しました。他のアプリを開いてお待ちください。")

    # プログレスバー
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.1) # 合計10秒
        bar.progress(i + 1)

    # 通知実行
    send_notification("タイマー完了", "10秒が経過しました！")
    st.success("通知を送信しました。")
