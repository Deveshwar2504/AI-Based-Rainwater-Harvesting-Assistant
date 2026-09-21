import streamlit as st

from rag_engine import get_answer
from calculator import (
    calculate_harvested_water,
    get_recommendation
)


st.set_page_config(
    page_title="Rainwater AI Assistant",
    page_icon="💧",
    layout="wide"
)


st.title("💧 AI-Based Rainwater Harvesting Assistant")

st.write(
    "An AI-powered sustainability assistant using "
    "Retrieval-Augmented Generation (RAG)."
)


tab1, tab2 = st.tabs(
    ["🤖 RAG Assistant", "💧 Rainwater Calculator"]
)


# ------------------------------------------------
# RAG ASSISTANT
# ------------------------------------------------

with tab1:

    st.header("Ask the Sustainability Assistant")

    question = st.text_area(
        "Enter your question",
        placeholder=(
            "Example: How does rooftop rainwater harvesting work?"
        )
    )

    if st.button("Get AI Recommendation"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Searching sustainability knowledge base..."
            ):

                try:
                    answer, sources = get_answer(question)
                except Exception as error:
                    st.error(
                        "Could not connect to Ollama. Start Ollama with "
                        "'ollama serve', confirm that llama3.2 is installed "
                        "with 'ollama list', and try again."
                    )
                    st.caption(f"Technical details: {error}")
                    answer, sources = None, []

            if answer is not None:
                st.subheader("AI Answer")

                st.write(answer)

                st.subheader("Retrieved Information")

                for i, source in enumerate(sources):

                    with st.expander(
                        f"Source {i + 1}"
                    ):

                        source_name = source.metadata.get(
                            "source", "Unknown source"
                        )
                        st.caption(source_name)
                        st.write(
                            source.page_content
                        )


# ------------------------------------------------
# CALCULATOR
# ------------------------------------------------

with tab2:

    st.header("Rainwater Harvesting Calculator")

    roof_area = st.number_input(
        "Roof Area (m²)",
        min_value=1.0,
        value=100.0
    )

    rainfall = st.number_input(
        "Annual Rainfall (mm)",
        min_value=1.0,
        value=800.0
    )

    runoff = st.number_input(
        "Runoff Coefficient",
        min_value=0.1,
        max_value=1.0,
        value=0.8,
        step=0.05
    )

    if st.button("Calculate"):

        volume_m3, litres = calculate_harvested_water(
            roof_area,
            rainfall,
            runoff
        )

        st.success(
            f"Estimated annual harvested water: "
            f"{litres:,.0f} litres"
        )

        st.info(
            f"Equivalent volume: "
            f"{volume_m3:.2f} m³"
        )

        recommendation = get_recommendation(
            litres,
            roof_area
        )

        st.subheader("Recommendation")

        st.write(recommendation)


st.divider()

st.caption(
    "Prototype for AI + Sustainability education. "
    "Engineering design should follow applicable local standards "
    "and site-specific professional guidance."
)