# streamlit_app.py
import streamlit as st
from model import SpellCheckerModule  # make sure model.py is lowercase 'model.py'

st.set_page_config(page_title="Spell & Grammar Checker", layout="centered")

# Instantiate once
@st.cache_resource
def get_checker():
    return SpellCheckerModule()

checker = get_checker()

st.title("📝 Spell & Grammar Checker")
st.markdown(
    "Use the text box to correct spelling or grammar. You can also upload a text file (.txt) for batch correction."
)

st.sidebar.header("Options")
mode = st.sidebar.radio("Select mode", ("Text", "File"))

if mode == "Text":
    st.subheader("Enter text")
    user_text = st.text_area("Type or paste text here", height=200)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Correct Spelling"):
            if not user_text.strip():
                st.warning("Please enter some text to correct.")
            else:
                with st.spinner("Correcting spelling..."):
                    corrected = checker.correct_spell(user_text)
                st.success("Spelling corrected:")
                st.code(corrected)
    with col2:
        if st.button("Correct Grammar"):
            if not user_text.strip():
                st.warning("Please enter some text to correct.")
            else:
                with st.spinner("Checking grammar..."):
                    corrected_grammar, mistakes, count = checker.correct_grammar(user_text)
                st.success(f"Grammar corrected ({count} suggestions):")
                st.code(corrected_grammar)
                if count > 0:
                    st.markdown("**Suggestions / Replacements (sample):**")
                    # show up to first 10 suggestions
                    for i, m in enumerate(mistakes[:10], start=1):
                        st.write(f"{i}. {m}")

elif mode == "File":
    st.subheader("Upload a text file (.txt)")
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
    if uploaded_file is not None:
        try:
            raw = uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            raw = uploaded_file.read().decode("latin-1", errors="ignore")

        st.markdown("**File preview (first 500 chars):**")
        st.code(raw[:500] + ("..." if len(raw) > 500 else ""))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Correct File Spelling"):
                with st.spinner("Correcting file spelling..."):
                    corrected_file = checker.correct_spell(raw)
                st.success("File spelling corrected:")
                st.code(corrected_file[:2000])  # limit output length
        with col2:
            if st.button("Correct File Grammar"):
                with st.spinner("Checking file grammar..."):
                    corrected_file_grammar, mistakes, count = checker.correct_grammar(raw)
                st.success(f"File grammar corrected ({count} suggestions):")
                st.code(corrected_file_grammar[:2000])
                if count > 0:
                    st.markdown("**Suggestions / Replacements (sample):**")
                    for i, m in enumerate(mistakes[:10], start=1):
                        st.write(f"{i}. {m}")

st.markdown("---")
st.caption("Powered by TextBlob and LanguageTool. Model persistence and heavy work run locally on your machine / deployed server.")
