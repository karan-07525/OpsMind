import streamlit as st
from agent import analyze_incident


st.set_page_config(
    page_title="OpsMind",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 OpsMind")
st.subheader("Production Incident Intelligence")

st.write(
    "OpsMind analyzes production incidents using AI and learns "
    "from previous incident outcomes through Hindsight memory."
)


st.divider()


# Incident input
st.header("🚨 Report an Incident")

service = st.text_input(
    "Service",
    placeholder="Example: Checkout API"
)

problem = st.text_input(
    "Problem",
    placeholder="Example: Intermittent HTTP 503 errors"
)

symptoms = st.text_area(
    "Symptoms",
    placeholder="Describe what engineers are observing..."
)


if st.button("🔍 Analyze Incident", type="primary"):

    if not service or not problem or not symptoms:
        st.warning("Please fill in all incident details.")

    else:

        incident = {
            "service": service,
            "problem": problem,
            "symptoms": symptoms
        }

        with st.spinner("OpsMind is analyzing the incident..."):

            try:
                result = analyze_incident(incident)

                st.success("Incident analysis completed!")

                st.divider()

                st.header("🤖 OpsMind Analysis")

                st.markdown(result)

            except Exception as e:

                st.error("Something went wrong while analyzing the incident.")

                st.code(str(e))