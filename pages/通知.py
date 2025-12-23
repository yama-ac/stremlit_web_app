import streamlit as st
import requests

def send_line(message, token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

st.title("LINE通知デモ")
token = "1QpyNMEQuWehUu05/WkZ8UI39dcYQGmSs8Yu4q2EgSf/4D+8SpkEi4VZstvWMFXHNY26kcCPG/xb8QTcVSrDwWFaCzIBlcr1IINJ1mgt5rP3vx2I+Y3x2pCFYXfimBRh8oVmiED55HeKrqpUasvgjAdB04t89/1O/w1cDnyilFU=" # 実際には st.secrets 等で管理を推奨

if st.button("LINEに通知を送る"):
    send_line("Streamlitアプリから通知が届きました！", token)
    st.toast("LINEに送信しました")
