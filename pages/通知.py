import streamlit as st

@st.dialog("重要な確認")
def confirm_action():
    st.write("この操作を実行するとデータが上書きされます。よろしいですか？")
    if st.button("実行する"):
        st.session_state.confirmed = True
        st.rerun()

st.title("ダイアログデモ")

if st.button("削除ボタン"):
    confirm_action()

if st.session_state.get("confirmed"):
    st.error("データを削除しました。")
    st.session_state.confirmed = False
