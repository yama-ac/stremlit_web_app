import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="デスクトップ通知", page_icon="🔔")

st.title("🔔 デスクトップ通知デモ")
st.write("ボタンを押して、他のアプリ（Excel等）を開いて待ってみてください。")

# 通知を送るためのJavaScript関数
def send_desktop_notification(title, body):
    js_code = f"""
    <script>
    function notifyMe() {{
        // ブラウザが通知をサポートしているか確認
        if (!("Notification" in window)) {{
            alert("このブラウザはデスクトップ通知をサポートしていません");
        }}
        // 許可を得ているか確認、得ていなければリクエスト
        else if (Notification.permission === "granted") {{
            new Notification("{title}", {{ body: "{body}" }});
        }}
        else if (Notification.permission !== "denied") {{
            Notification.requestPermission().then(function (permission) {{
                if (permission === "granted") {{
                    new Notification("{title}", {{ body: "{body}" }});
                }
            }});
        }}
    }}
    notifyMe();
    </script>
    """
    # 0pxのコンポーネントとしてJavaScriptを実行
    components.html(js_code, height=0)

if st.button('10秒タイマーを開始'):
    st.info("タイマーを開始しました。他のアプリに切り替えても大丈夫です。")

    # 10秒カウントダウン
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.1)
        progress_bar.progress(i + 1)

    # OSの通知を実行
    send_desktop_notification("時間です！", "10秒が経過しました。アプリを確認してください。")
    st.success("デスクトップ通知を送信しました。")
