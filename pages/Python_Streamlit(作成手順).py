import streamlit as st
from PIL import Image

# ページ設定をワイドモードにする
st.set_page_config(layout="wide")

st.title("Python：Stremlit")

code = """
# 仮想環境構築
python3 -m venv venv

# 仮想環境をアクティブにする
source venv/bin/activate

# streamlitインストール
pip install streamlit

# Top.pyのファイルを作成
Top.py

# app.pyのコードを実行
streamlit run Top.py

"""

st.code(code, language="python")
