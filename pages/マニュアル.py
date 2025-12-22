import streamlit as st
from PIL import Image

# ページ設定をワイドモードにする
st.set_page_config(layout="wide")

st.title("基本的な使い方")

# 1. タイトル
st.title("これは st.title です")

# 2. ヘッダー
st.header("セクション1: st.header")

# 3. サブヘッダー
st.subheader("1-1. st.subheader")

# 4. マークダウン（自由に装飾可能）
st.markdown("""
**st.markdown** を使うと、以下のようなことができます。
* 箇条書き
* [リンクの作成](https://streamlit.io)
* *斜体* や **太字**
""")

# 5. コード表示
st.code("print('Hello, Streamlit!')", language='python')

# 6. 注釈（フッターによく使います）
st.caption("これは st.caption です。注釈やクレジット表記に便利です。")

# ページ内のさらに細かい分類はタブを使う
tab1, tab2, tab3 = st.tabs(["基本情報", "詳細データ", "履歴"])

image = Image.open("画像/sample.png")
st.image(image, width=800)

st.success("成功しました！")
st.info("お知らせです")
st.warning("注意してください")
st.error("エラーが発生しました")

st.title("アンケートフォーム")

# フォームの作成
with st.form("my_form"):
    name = st.text_input("お名前")
    age = st.slider("年齢", 0, 100)
    category = st.selectbox("興味のある分野", ["プログラミング", "デザイン", "マーケティング"])

    # 送信ボタン（これがないとエラーになります）
    submitted = st.form_submit_button("送信する")

    if submitted:
        st.write(f"送信完了！こんにちは、{name}さん。")

# 2つのカラムを作成
with st.container(border=True):
    left_column, right_column = st.columns(2)

    # 左側の操作
    with left_column:
        st.header("← 左側のエリア")

    # 右側の操作
    with right_column:
        st.header("右側のエリア →")


# 左を1、右を3の比率で分割
with st.container(border=True):
    col1, col2 = st.columns([1, 3])

    with col1:
        st.write("短いエリア（1）")
        st.selectbox("選択", ["A", "B", "C"])

    with col2:
        st.write("長いエリア（3）")
        st.line_chart([10, 20, 15, 30], use_container_width=True)

    left, right = st.columns(2, gap="large")


st.title("枠線のサンプル")
# border=True を指定するだけで枠線がつきます
with st.container(border=True):
    st.subheader("枠線の中のコンテンツ")
    st.write("ここにある要素はすべて一つの枠で囲まれます。")
