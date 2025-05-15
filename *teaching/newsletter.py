import streamlit as st
from datetime import datetime
import pytz

# --------------------------------------------------
# 📰  Sample newsletter used as a fallback preview
# --------------------------------------------------
sample_newsletter = {
    "week_start": datetime(2025, 4, 28),
    "headline": "🛡️ The Bedrock Bulletin – Chaos & Conquest Edition!",
    "subheadline": "Week of April 28 – May 4, 2025",
    "sections": [
        {
            "title": "Monday Mayhem",
            "body": (
                "Spawn was rocked by back‑to‑back creeper blasts after **K1ngLeo** tried "
                "to expand his redstone shop without lighting it up. "
                "**PixelPenguin** swooped in to rescue the dropped gunpowder—and "
                "half the diamonds.\n\n"
                "Meanwhile, **NettleFox** started tunneling a secret rail line under "
                "the shopping district. Rumor is it leads straight to the vault…"
            ),
        },
        {
            "title": "Build Showcase 🏰",
            "body": (
                "**BlockBruh** finished a *1:1 scale* dragon skeleton in the Mesa. "
                "It flaps its wings every sunset thanks to 2,300 slime blocks and "
                "a questionable amount of lag. Visit at X ‑1420 / Z 680!"
            ),
        },
        {
            "title": "PvP Headlines ⚔️",
            "body": (
                "The **Nether Lords** (Player3’s faction) ambushed **Overworld Union** "
                "in the basalt delta. Final score: 7‑2, one netherite chestplate "
                "misplaced, and a lot of salty chat logs."
            ),
        },
        {
            "title": "Quote of the Week",
            "body": (
                "> “It’s not stealing if they log off first.” — **SneakySalmon**, seconds "
                "before the server reboot."
            ),
        },
        {
            "title": "Looking Ahead 🔮",
            "body": (
                "- **Friday**: Elytra course speed‑run tournament (prize: mending book)\n"
                "- **Weekend**: Map‑wide Easter‑egg hunt (1.20.5’s armor trims are hidden everywhere)\n"
                "- Rumor: **K1ngLeo** is plotting TNT‑fueled revenge… stay tuned."
            ),
        },
    ],
}


def show(database):
    """Display the weekly SMP newsletter in a classic newspaper layout."""

    # ----------  Style ---------- #
    st.markdown(
        """
        <style>
        .news-container { max-width: 900px; margin: auto; font-family: 'Times New Roman', serif; }
        .news-header   { text-align: center; font-size: 48px; font-weight: 800; margin-bottom: 0; }
        .news-subheader{ text-align: center; font-size: 22px; margin-top: 0; margin-bottom: 40px; font-style: italic; }
        .section-title { font-size: 28px; font-weight: 700; border-bottom: 2px solid #000; margin-top: 30px; }
        .article       { text-align: justify; font-size: 18px; line-height: 1.65; margin-bottom: 20px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📰 SMP Times")

    # ----------  Retrieve editions ---------- #
    try:
        newsletters_ref = (
            database.collection("newsletters")
            .order_by("week_start", direction="DESCENDING")
            .limit(10)
        )
        docs = newsletters_ref.get()
    except Exception as e:
        st.error(f"Could not load newsletters: {e}")
        docs = []

    # ----------  Fallback sample if Firestore is empty ---------- #
    if not docs:
        SampleDoc = type("SampleDoc", (), {"to_dict": lambda self: sample_newsletter})
        docs = [SampleDoc()]
        st.warning("Showing sample newsletter (no data in Firestore yet).")

    # ----------  Build dropdown list ---------- #
    tz = pytz.timezone("America/Los_Angeles")
    editions: list[tuple[str, dict]] = []
    for d in docs:
        data = d.to_dict()
        start = data.get("week_start")
        label = (
            start.astimezone(tz).strftime("%B %d, %Y") if isinstance(start, datetime) else str(start)
        )
        editions.append((label, data))

    labels = [lbl for lbl, _ in editions]
    selected_label = st.sidebar.selectbox("Edition", labels, index=0)
    selected_newsletter = next(data for lbl, data in editions if lbl == selected_label)

    # ----------  Render newsletter ---------- #
    headline = selected_newsletter.get("headline", "SMP Weekly Recap")
    subheadline = selected_newsletter.get("subheadline", f"Week of {selected_label}")
    sections = selected_newsletter.get("sections", [])
    if isinstance(sections, str):
        sections = [{"title": "Full Story", "body": sections}]

    st.markdown(
        f"""
        <div class=\"news-container\">
            <div class=\"news-header\">{headline}</div>
            <div class=\"news-subheader\">{subheadline}</div>
        """,
        unsafe_allow_html=True,
    )

    for section in sections:
        title = section.get("title", "")
        body = section.get("body", "")
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="article">{body}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
