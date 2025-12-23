import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="熊本県 鉄道運行状況", page_icon="🚃")

st.title("🚃 熊本県 鉄道運行状況")
st.caption("Yahoo!路線情報の九州エリアから情報を取得します")

def get_train_status():
    url = "https://transit.yahoo.co.jp/diainfo/area/7" # 九州エリアのURL
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    lines = []
    # 熊本関連のキーワードでフィルタリング
    target_keywords = ["JR九州", "熊本", "市電", "阿蘇", "肥薩"]

    # 運行情報のテーブルを取得
    table = soup.find("div", class_="elmTblKyuhon")
    if table:
        for tr in table.find_all("tr")[1:]: # ヘッダー以外
            tds = tr.find_all("td")
            if len(tds) >= 3:
                name = tds[0].text.strip()
                status = tds[1].text.strip()
                detail = tds[2].text.strip()

                # 熊本に関連する路線のみ抽出
                if any(k in name for k in target_keywords):
                    lines.append({
                        "路線名": name,
                        "状況": status,
                        "詳細": detail
                    })
    return lines

if st.button("情報を更新"):
    data = get_train_status()
    if data:
        df = pd.DataFrame(data)

        # 状況に応じて色分け
        def color_status(val):
            color = 'red' if '見合わせ' in val or '遅れ' in val else 'green'
            return f'color: {color}'

        st.table(df.style.applymap(color_status, subset=['状況']))
    else:
        st.info("現在、熊本エリアに目立った遅延・運休情報はありません。")

st.info("※この情報はYahoo!路線情報の情報を元にしています。正確な情報は各公式サイトをご確認ください。")
