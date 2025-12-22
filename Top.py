# Gemini
# https://gemini.google.com/app/df8cdd6bd9d59dcc?hl=ja

import streamlit as st
from PIL import Image

# ページ設定をワイドモードにする
st.set_page_config(layout="wide")

# サイドバーに画像を表示
st.sidebar.image("画像/sample.png", caption="Version 1.0")
st.sidebar.title("管理パネル")

# グループ1: 検索・フィルタ
with st.sidebar.container(border=True):
    st.write("🔍 **フィルタ設定**")
    date = st.date_input("日付を選択")
    category = st.multiselect("カテゴリ", ["A", "B", "C"])

# グループ2: 詳細設定（普段は隠しておく）
with st.sidebar.expander("🛠️ 詳細オプション"):
    st.slider("感度設定", 0, 100, 50)
    st.checkbox("ダークモードを優先")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.button("保存", use_container_width=True)
with col2:
    st.button("破棄", use_container_width=True)

# サイドバーの背景色を薄い青色に変える例
# st.markdown(
#     """
#     <style>
#         [data-testid="stSidebar"] {
#             background-color: skyblue;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.title("メインページ")

# ボタン形式のリンク
st.link_button("Googleを開く", "https://www.google.com")

# Markdown形式でリンクを作成（相対パスを指定）
st.markdown("[分析ページへ移動する](/Python_Streamlit)")

# ボタンで遷移させる場合
if st.button("Python_Streamlit(作成手順)　へ移動する"):
    st.switch_page("pages/Python_Streamlit.py")


# 選択肢を準備（表示名：ファイルパス）
pages = {
    "--- ページを選んでください ---": None,
    "📊 Python_Streamlit(作成手順)": "pages/Python_Streamlit(作成手順).py",
}
# テキストを選択させる
selected_label = st.selectbox("移動先のテキストを選択してください", list(pages.keys()))

# 選択されたら即座に遷移
target_page = pages[selected_label]
if target_page:
    st.switch_page(target_page)
