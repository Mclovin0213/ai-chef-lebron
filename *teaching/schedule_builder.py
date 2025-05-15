# pages/schedule_builder.py

import json
from datetime import datetime

import streamlit as st
from firebase_admin import firestore

# ---- OpenAI helper ---------------------------------------------------------
from ai_template import get_json_response  # ↩️ adjust if needed

# ---- Constants -------------------------------------------------------------

SCHEDULE_HELPER_SYSTEM_PROMPT = """
You are a smart scheduling assistant called “Schedule_Helper”. Your job is to create a clear, manageable weekly schedule for the user based on the information they provide.

When building the schedule:
* Prioritize imminent due dates (homework, projects, tests).
* Spread study sessions and work evenly through the week to avoid cramming.
* Insert short breaks and leave buffer time; never overload any single day.
* Categorize each block as Classes, Homework, Projects, Tests/Quizzes, or Other.
* Suggest specific time blocks (e.g. “Monday 16:00‑17:00 – Study for Math test”).

Output rules (very important):
1. Respond only with valid JSON (no extra text).
2. The JSON must have exactly two top‑level keys:
   • "events" – an array of event objects compatible with streamlit‑calendar.
   • "motivational_message" – a single inspiring sentence.
3. Each event object must contain:
   {
     "title": "📚 English essay",      // short label, emoji optional
     "start": "2025-05-07T14:00:00",   // ISO‑8601
     "end":   "2025-05-07T16:00:00",   // ISO‑8601
     "allDay": false,                  // optional, default false
     "category": "Homework"            // one of the five categories above
   }
4. Use the user’s local timezone (America/Los_Angeles) when generating start and end.
5. Ensure every event’s duration is realistic (30‑ to 120‑minute study blocks work best).
"""

# ----------------------------------------------------------------------------

def show(database: firestore.Client):
    """Render the *Build weekly schedule* page."""

    st.title("🗓️  Build your weekly study schedule")

    # ---- Auth gate ---------------------------------------------------------
    if "user" not in st.session_state:
        st.warning("Please log in first to generate and save a schedule.")
        st.stop()

    user = st.session_state["user"]
    uid = user["localId"]

    # ---- Input form --------------------------------------------------------
    st.markdown(
        """
        **Describe everything you need to get done next week** – classes, homework,
        project deadlines, tests, sports practice, part‑time job shifts…
        The more detail you give, the better the schedule.
        """
    )

    default_example = (
        "Classes: Math MWF 10‑11 AM, English Tu/Th 1‑2:30 PM.  "
        "Homework: Math problem set due Friday.  "
        "Projects: History presentation due next Monday.  "
        "Tests: Chemistry quiz Thursday.  "
        "Other: Soccer practice Wed 5‑6 PM."
    )

    user_prompt = st.text_area("Your upcoming week", value="", placeholder=default_example, height=200)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        generate_btn = st.button("🪄 Generate schedule", disabled=not user_prompt.strip())
    with col_b:
        clear_btn = st.button("🔄 Clear")
        if clear_btn:
            st.rerun()

    # ---- Call OpenAI & save -----------------------------------------------
    if generate_btn:
        with st.spinner("Calling Schedule_Helper …"):
            try:
                # 1️⃣  Call the model
                result = get_json_response(SCHEDULE_HELPER_SYSTEM_PROMPT, user_prompt)

                # 2️⃣  Basic validation / normalisation
                events = result.get("events", [])
                if not isinstance(events, list):
                    raise ValueError("AI response missing 'events' array")

                # ensure ISO‑8601 with 'T' (just in case)
                for ev in events:
                    for key in ("start", "end"):
                        ev[key] = ev[key].replace(" ", "T")
                    ev.setdefault("allDay", False)

                # 3️⃣  Persist to Firestore (merge keeps existing fields)
                database.collection("users").document(uid).set(
                    {
                        "events": events,
                        "motivational_message": result.get("motivational_message", "")
                    },
                    merge=True,
                )

            except Exception as e:
                st.error(f"Failed to generate schedule: {e}")
                st.stop()

        st.success("Schedule saved! Head to the *Calendar* page to see it.")

        with st.expander("AI‑generated events"):
            st.json(events)
            st.write(result.get("motivational_message", ""))
