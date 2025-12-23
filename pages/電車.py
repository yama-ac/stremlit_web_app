import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ページの設定
st.set_page_config(page_title="本日の熊本県運行状況", layout="wide")

st.title("🚃 今日の熊本県 鉄道運行状況")
st.write(f"取得日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")

# 運行情報を取得する関数
def get_today_status():
    # Yahoo!路線情報（九州エリア）
    url = "https://transit.yahoo.co.jp/diainfo/area/7"

    try:
        res = requests.get(url)
        res.raise_for_status() # エラーがあれば例外を出す
        soup = BeautifulSoup(res.text, "html.parser")

        # 熊本県に関連する路線のキーワード
        target_keywords = ["JR九州", "熊本", "阿蘇", "肥薩", "三角線", "鹿児島本線", "九州新幹線"]

        results = []

        # 運行情報のテーブルを探す
        table = soup.find("div", class_="elmTblKyuhon")
        if not table:
            return None

        rows = table.find_all("tr")
        for row in rows[1:]: # ヘッダーを飛ばす
            cols = row.find_all("td")
            if len(cols) >= 3:
                line_name = cols[0].text.strip()
                status = cols[1].text.strip()
                detail = cols[2].text.strip()

                # キーワードに合致する路線のみ保存
                if any(k in line_name for k in target_keywords):
                    results.append({
                        "路線名": line_name,
                        "運行状況": status,
                        "詳細内容": detail
                    })
        return results

    except Exception as e:
        st.error(f"データ取得中にエラーが発生しました: {e}")
        return None

# メイン処理
status_data = get_today_status()

if status_data:
    # データを表形式（DataFrame）にする
    df = pd.DataFrame(status_data)

    # 状況が「平常運転」以外の場合に背景色を変える装飾（任意）
    def highlight_status(val):
        color = '#ffcccc' if '見合わせ' in val or '遅れ' in val or '運休' in val else 'white'
        return f'background-color: {color}'

    # 表示
    st.subheader("現在の状況")
    st.table(df) # シンプルな表として表示

else:
    st.success("現在、熊本県内の対象路線に目立った遅延・運休情報はありません。")

st.divider()
st.caption("※データ元：Yahoo!路線情報。この表示は一時的なもので、再読み込みすると最新の状態に更新されます。")
