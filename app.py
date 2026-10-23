
import re
import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="StudySpark AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 StudySpark AI")
st.write("Turn your study notes into revision material.")

notes = st.text_area(
    "Paste your study notes here",
    height=220,
    placeholder="Paste your chapter notes here..."
)

def make_summary(text, limit=5):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= limit:
        return sentences

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    frequency = Counter(words)
    scored = []

    for index, sentence in enumerate(sentences):
        terms = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        score = sum(frequency[word] for word in terms)
        scored.append((score, index, sentence))

    selected = sorted(scored, reverse=True)[:limit]
    selected.sort(key=lambda item: item[1])
    return [item[2] for item in selected]

if st.button("✨ Generate revision pack"):
    if len(notes.split()) < 10:
        st.warning("Please enter at least 10 words.")
    else:
        summary = make_summary(notes)

        st.subheader("📝 Summary")
        for sentence in summary:
            st.write("• " + sentence)

        st.subheader("❓ Practice questions")
        for i, sentence in enumerate(summary, 1):
            st.write(f"{i}. What is the main idea of this statement?")
            with st.expander("View study note"):
                st.write(sentence)

        st.info(
            "Prototype version: this app uses basic text processing, "
            "not a real AI model yet. Check the output against your notes."
        )
