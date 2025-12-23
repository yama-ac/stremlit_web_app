import streamlit as st
import time
import streamlit.components.v1 as components

st.title("バックグラウンド通知アプリ")

# ブラウザの通知機能を呼び出すためのJavaScript
def send_browser_notification(title, body):
    js_code = f"""
    <script>
    function notify() {{
        if (Notification.permission === "granted") {{
            new Notification("{title}", {{ body: "{body}" }});
        }} else if (Notification.permission !== "denied") {{
            Notification.requestPermission().then(permission => {{
                if (permission === "granted") {{
                    new Notification("{title}", {{ body: "{body}" }});
                }}
            }});
        }}
    }}
    // 実行
    notify();
    </script>
    """
    components.html(js_code, height=0)

if st.button('10秒後にOS通知を送る'):
    st.info("タイマーを開始しました。別のタブで作業していてもOKです。")

    # 10秒待機
    time.sleep(10)

    # 通知を実行
    send_browser_notification("時間です！", "10秒が経過しました。")
    st.success("通知を送りました。")
