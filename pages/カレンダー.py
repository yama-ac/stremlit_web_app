import streamlit as st

st.title("Googleカレンダーの表示")

# Googleカレンダーの「設定と共有」から取得した公開URL（iframeのsrc部分）
calendar_url = "https://calendar.google.com/calendar/embed?src=0613061ae80a670356c6d4b09643f5ac0b5d32a394568be7b8ccd90fc05c88cb@group.calendar.google.com"

# st.components.v1.iframe(calendar_url, height=600, scrolling=True)

st.markdown(
    f'<iframe src="{calendar_url}" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>',
    unsafe_allow_html=True
)

