import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="StudySpark AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 StudySpark AI")
st.write("Your AI-powered study companion.")

notes = st.text_area(
    "Paste your study notes",
    max_chars=6000,
    height=220,
    placeholder="Paste your chapter notes here..."
)

task = st.selectbox(
    "Choose what to generate",
    [
        "Summary",
        "Quiz questions with answers",
        "Flashcards",
        "Complete revision pack"
    ]
)

if st.button("✨ Generate with AI", type="primary"):
    if len(notes.split()) < 10:
        st.warning("Please enter at least 10 words of notes.")
    else:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
            client = OpenAI(api_key=api_key)

            prompts = {
                "Summary": "Summarize these notes in simple language.",
                "Quiz questions with answers": "Create five quiz questions with answers and brief explanations.",
                "Flashcards": "Create ten question-and-answer flashcards.",
                "Complete revision pack": "Create a summary, five quiz questions with answers, and five flashcards."
            }

            with st.spinner("Creating your study material..."):
                response = client.responses.create(
                    model="gpt-5.5",
                    instructions=(
                        "You are StudySpark, a careful study assistant. "
                        "Use the student's notes as your source. "
                        "Do not invent facts. Use clear headings."
                    ),
                    input=prompts[task] + "\n\nSTUDENT NOTES:\n" + notes,
                    max_output_tokens=1200
                )

            st.subheader("Your revision material")
            st.markdown(response.output_text)
            st.caption("Check important facts against your textbook.")

        except Exception:
            st.error(
                "AI setup failed. Check your API key, model access, "
                "and API billing settings."
            )
