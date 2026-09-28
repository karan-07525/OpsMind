import uuid
import streamlit as st

from agent import analyze_incident
from hindsight_memory import learn_from_outcome, get_hindsight_memories


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="OpsMind",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "learning_history" not in st.session_state:
    st.session_state["learning_history"] = []

if "analysis" not in st.session_state:
    st.session_state["analysis"] = None

if "incident" not in st.session_state:
    st.session_state["incident"] = None


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 OpsMind")
st.subheader("Production Incident Intelligence")

st.write(
    "OpsMind analyzes production incidents using AI and learns "
    "from real engineering outcomes through Hindsight memory."
)
st.info(
    "🔄 LEARNING LOOP: "
    "Incident → Recall Experience → Recommend → "
    "Engineer Outcome → Learn → Improve Next Response"
)
st.markdown(
    """
    ### 🧠 How OpsMind Learns

    **🚨 Incident**
    ↓
    **🔎 Recall Experience**
    ↓
    **🤖 AI Recommendation**
    ↓
    **👨‍💻 Engineer Outcome**
    ↓
    **💾 Hindsight Memory**
    ↓
    **📈 Better Future Response**
    """
)
st.divider()


# --------------------------------------------------
# Incident Report
# --------------------------------------------------

st.header("🚨 Report an Incident")

service = st.text_input(
    "Service",
    placeholder="Example: Checkout API, Payment API, Auth Service"
)

problem = st.text_input(
    "Problem",
   placeholder="Example: Intermittent HTTP 503 errors during traffic spikes"
)

symptoms = st.text_area(
    "Symptoms",
    placeholder="Example: Requests become slow during peak traffic, then return HTTP 503 errors..."
)


if st.button("🔍 Analyze Incident", type="primary"):

    if not service or not problem or not symptoms:
        st.warning("Please fill in all incident details.")

    else:
        incident = {
            "id": f"INC-{uuid.uuid4().hex[:6].upper()}",
            "service": service,
            "problem": problem,
            "symptoms": symptoms
        }

        with st.spinner("OpsMind is recalling experience and analyzing..."):

            try:
                result = analyze_incident(incident)

                st.session_state["incident"] = incident
                st.session_state["analysis"] = result

            except Exception as e:
                st.error("Something went wrong while analyzing the incident.")
                st.exception(e)# --------------------------------------------------
# Hindsight Memory
# --------------------------------------------------

if st.session_state.get("hindsight_memories"):

    st.divider()

    st.header("🧠 Hindsight Memory")

    st.write(
        "These memories were retrieved from OpsMind's long-term "
        "Hindsight memory for this incident."
    )

    for i, memory in enumerate(
        st.session_state["hindsight_memories"],
        start=1
    ):

        with st.expander(f"Memory {i}"):

            st.write(memory)


# --------------------------------------------------
# AI Analysis
# --------------------------------------------------


if st.session_state["analysis"]:

    st.divider()

    st.header("🤖 OpsMind Analysis")

    st.markdown(
        st.session_state["analysis"]
    )


    # --------------------------------------------------
    # Engineer Outcome
    # --------------------------------------------------

    st.divider()

st.header("🧑‍💻 What Actually Happened?")

st.write(
    "OpsMind learns from the engineer's real-world outcome, "
    "not just its own recommendation."
)

with st.form("engineer_outcome_form", clear_on_submit=True):

    engineer_action = st.text_area(
        "What action did the engineer take?",
        placeholder=(
            "Example: Increased the database connection pool "
            "from 50 to 150."
        )
    )

    outcome = st.radio(
        "What was the outcome?",
        ["RESOLVED", "FAILED"],
        horizontal=True
    )

    lesson = st.text_area(
        "What should OpsMind remember for future incidents?",
        placeholder=(
            "Example: Check database connection pool exhaustion "
            "before restarting the service."
        )
    )

    teach_button = st.form_submit_button(
        "🧠 Teach OpsMind"
    )


if teach_button:

    if not engineer_action or not lesson:

        st.warning(
            "Please enter the engineer action and lesson."
        )

    else:

        incident = st.session_state["incident"]

        try:

            learn_from_outcome(
                incident_id=incident["id"],
                action=engineer_action,
                outcome=outcome,
                lesson=lesson
            )

            learning_record = {
                "incident_id": incident["id"],
                "service": incident["service"],
                "problem": incident["problem"],
                "action": engineer_action,
                "outcome": outcome,
                "lesson": lesson
            }

            st.session_state["learning_history"].append(
                learning_record
            )

            st.success(
                "🧠 OpsMind learned from this incident!"
            )

            st.info(
                f"Incident {incident['id']} → "
                f"{outcome} → memory retained in Hindsight."
            )

        except Exception as e:

            st.error(
                "Could not save the learning to Hindsight."
            )

            st.code(str(e))
# --------------------------------------------------
# Memory Evolution
# --------------------------------------------------

if st.session_state["learning_history"]:

    st.divider()

    st.header("🧠 Memory Evolution")

    st.write(
        "OpsMind turns real engineering outcomes into persistent "
        "experience that can influence future incident responses."
    )

    for record in reversed(
        st.session_state["learning_history"]
    ):

        if record["outcome"] == "RESOLVED":
            outcome_icon = "✅"
            outcome_label = "RESOLVED"
        else:
            outcome_icon = "❌"
            outcome_label = "FAILED"

        with st.expander(
            f"{outcome_icon} {record['incident_id']} — "
            f"{record['service']} — {outcome_label}"
        ):

            st.markdown("### 🔎 Incident")

            st.write(
                f"**Problem:** {record['problem']}"
            )

            st.markdown("### 👨‍💻 Engineer Action")

            st.write(
                record["action"]
            )

            st.markdown("### 📊 Outcome")

            st.write(
                f"{outcome_icon} **{outcome_label}**"
            )

            st.markdown("### 💡 Lesson Learned")

            st.info(
                record["lesson"]
            )

            st.markdown("### 🔄 How This Improves OpsMind")

            if record["outcome"] == "RESOLVED":

                st.success(
                    "This successful experience can be recalled "
                    "when OpsMind analyzes similar future incidents."
                )

            else:

                st.warning(
                    "This failed experience can be recalled so "
                    "OpsMind can warn engineers against repeating "
                    "the same ineffective action."
                )

    # --------------------------------------------------
# Why I Remember This
# --------------------------------------------------

st.divider()

st.header("🔎 Why I Remember This")

st.write(
    "OpsMind uses recorded engineering outcomes as future "
    "experience. Successful and failed actions are both retained."
)

successful = []
failed = []

seen_successful = set()
seen_failed = set()

for r in st.session_state["learning_history"]:

    key = (
        r["incident_id"],
        r["action"],
        r["lesson"]
    )

    if r["outcome"] == "RESOLVED":

        if key not in seen_successful:
            successful.append(r)
            seen_successful.add(key)

    elif r["outcome"] == "FAILED":

        if key not in seen_failed:
            failed.append(r)
            seen_failed.add(key)


col1, col2 = st.columns(2)


with col1:

    st.subheader("✅ Successful Experience")

    if successful:

        for record in successful:

            with st.container(border=True):

                st.write(
                    f"**{record['incident_id']}**"
                )

                st.write(
                    f"**Action:** {record['action']}"
                )

                st.write(
                    f"**Lesson:** {record['lesson']}"
                )

    else:

        st.info(
            "No successful learning recorded yet."
        )


with col2:

    st.subheader("❌ Failed Experience")

    if failed:

        for record in failed:

            with st.container(border=True):

                st.write(
                    f"**{record['incident_id']}**"
                )

                st.write(
                    f"**Action:** {record['action']}"
                )

                st.write(
                    f"**Lesson:** {record['lesson']}"
                )

    else:

        st.info(
            "No failed learning recorded yet."
        )