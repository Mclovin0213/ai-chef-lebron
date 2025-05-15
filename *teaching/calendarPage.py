import streamlit as st
from streamlit_calendar import calendar
from datetime import date, datetime, time, timedelta


def show(database):
    """Weekly schedule page for Sarah's study planner.

    * Displays a **time‑grid week** (Mon‑Sun) so the whole week is visible at once.
    * Lets the student drag‑and‑drop or select slots to create homework / study / break blocks.
    * Events live in ``st.session_state['schedule_events']`` and can optionally be saved to Firestore.
    """

    # ---------- greeting ----------
    user = st.session_state.get("user")
    username = ""
    if user:
        profile = (
            database.collection("users")
            .document(user["localId"])
            .get()
            .to_dict()
        )
        username = profile.get("username", "")
    st.title(f"Welcome {username or 'there'} – Weekly schedule")

    events = database.collection("users").document(user["localId"]).get()

    st.write(events)

    # ---------- state ----------
    if "schedule_events" not in st.session_state:
        # provide a few sample blocks so the calendar isn't empty the first time
        st.session_state["schedule_events"] = [
            {
                "title": "🍎 Math HW",
                "start": "2025-05-05T16:00:00",
                "end": "2025-05-05T17:00:00",
            },
            {
                "title": "📚 English essay",
                "start": "2025-05-07T14:00:00",
                "end": "2025-05-07T16:00:00",
            },
            {
                "title": "🏀 Break",
                "start": "2025-05-06T18:00:00",
                "end": "2025-05-06T19:00:00",
            },
        ]

    events = st.session_state["schedule_events"]

    # ---------- calendar ----------
    calendar_options = {
        "initialView": "timeGridWeek",  # full week view
        "firstDay": 1,                   # Monday first
        "editable": True,
        "selectable": True,
        "nowIndicator": True,
        "slotMinTime": "06:00:00",
        "slotMaxTime": "23:00:00",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "",
        },
        # nice week‑range title e.g. "May 5 – May 11, 2025"
        "titleFormat": {"week": "MMM d - MMM d, yyyy"},
    }

    response = calendar(events=events, options=calendar_options, key="schedule")

    # ---------- callbacks ----------
    if response:
        cb = response.get("callback")
        if cb == "select":
            sel = response["select"]
            with st.sidebar.form("add_event_from_select"):
                st.subheader("Add a new task")
                title = st.text_input("Title", key="title_from_select")
                all_day = st.checkbox("All‑day", value=sel["allDay"])
                confirm = st.form_submit_button("Add")
                if confirm and title:
                    events.append(
                        {
                            "title": title,
                            "start": sel["start"],
                            "end": sel["end"],
                            "allDay": all_day,
                        }
                    )
                    st.rerun()
        elif cb == "eventChange":
            st.toast("Schedule updated 👍")
