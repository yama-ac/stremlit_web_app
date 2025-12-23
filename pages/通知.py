import streamlit as st
import streamlit.components.v1 as components
import time

st.title("OS通知デバッグ版")

# 現在のブラウザの通知許可状態をチェックするJavaScript
check_permission_js = """
<script>
    const permission = Notification.permission;
    window.parent.postMessage({type: 'notification_status', status: permission}, "*");
</script>
"""

def send_os_notification(title, body):
    js_code = f"""
    <script>
    function notify() {{
        if (Notification.permission === "granted") {{
            new Notification("{title}", {{ body: "{body}" }});
        }} else {{
            Notification.requestPermission().then(p => {{
                if (p === "granted") {{
                    new Notification("{title}", {{ body: "{body}" }});
                }} else {{
                    alert("通知が拒否されています。ブラウザの設定を確認してください。ステータス: " + p);
                }}
            }});
        }}
    }}
    notify();
    </script>
    """
    components.html(js_code, height=0)

# ボタン
if st.button("10秒後に通知を送る"):
    st.info("10秒カウントダウン中... その間に他のタブやアプリに切り替えてみてください。")

    # プログレスバーで時間を視覚化
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.1)
        bar.progress(i + 1)

    send_os_notification("タイマー終了", "10秒経ちました！")
    st.success("通知命令を送信しました。")

st.divider()
st.caption("※通知が出ない場合は、URLバー横の鍵マークから『通知』を許可してください。")
