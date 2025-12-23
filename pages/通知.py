import streamlit as st
import streamlit.components.v1 as components

def send_os_notification(title, body):
    js_code = f"""
    <script>
    if (Notification.permission === "granted") {{
        new Notification("{title}", {{ body: "{body}" }});
    }} else {{
        Notification.requestPermission().then(p => {{
            if (p === "granted") {{ new Notification("{title}", {{ body: "{body}" }}); }}
        }});
    }}
    </script>
    """
    components.html(js_code, height=0)

st.title("OS通知デモ")
if st.button("5秒後にOS通知を送る"):
    import time
    time.sleep(5)
    send_os_notification("タイマー終了", "別のアプリを見ていても届きます！")
