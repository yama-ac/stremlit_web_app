import streamlit as st
from streamlit_calendar import calendar

st.title("Streamlit カレンダーデモ")

calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    },
    "initialView": "dayGridMonth",
}

calendar_events = [
    {
        "title": "ミーティング",
        "start": "2023-12-25T10:00:00",
        "end": "2023-12-25T11:00:00",
    },
    {
        "title": "ランチ",
        "start": "2023-12-26",
        "allDay": "true",
    }
]

state = calendar(events=calendar_events, options=calendar_options)
st.write(state)
