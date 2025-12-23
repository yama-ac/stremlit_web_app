import streamlit as st
import requests

def send_line(message, token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

st.title("LINE通知デモ")
token = "LJeAQc+2nmVIAL/rPm9RJIm7obZdCmPFkmkGBuNXJq8dkvqXqFrpbyPaBE5B5Gxy/cnKt+Fj6mTU/VtGSPvacrwZCrZcHvBiYtUPwKuVyH78KknAV1OemCHJQ8vllfsTAsw9F/9rGqBJaJ4Z7lziwwdB04t89/1O/w1cDnyilFU=" # 実際には st.secrets 等で管理を推奨

if st.button("LINEに通知を送る"):
    send_line("Streamlitアプリから通知が届きました！", token)
    st.toast("LINEに送信しました")
