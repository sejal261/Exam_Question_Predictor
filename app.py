
import streamlit as st
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# ------------------------------------
# PAGE CONFIGURATION
# ------------------------------------
st.set_page_config(
    page_title="Exam Question Predictor",
    page_icon="📚",
    layout="wide"
)

# ------------------------------------
# WEBSITE STYLING
# ------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #DCEBFF, #EEF5FF);
}

div[data-testid="stAppViewContainer"] {
    background: transparent;
}

.stButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #1D4ED8 !important;
    color: white !important;
}

div[data-testid="stFileUploader"] {
    background-color: rgba(255, 255, 255, 0.65);
    border-radius: 12px;
    padding: 10px;
}

div[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.75);
    padding: 16px;
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background-color: rgba(255, 255, 255, 0.72);
    border-radius: 12px;
    border: 1px solid #BFDBFE;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------
# TITLE AND INTRODUCTION
# ------------------------------------
st.markdown(
    '<h1 style="color:#1E3A8A;">📚 Exam Question Predictor</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<h3 style="color:#2563EB;">Generate Practice Questions From Your Syllabus</h3>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="color:#334155;">Upload your syllabus PDF to extract units, '
    'identify important keywords, and generate practice questions.</p>',
    unsafe_allow_html=True
)

st.divider()


# ------------------------------------
# PDF TEXT EXTRACTION
# ------------------------------------
def extract_text(pdf_file):
    text = ""

    with fitz.open(
        stream=pdf_file.getvalue(),
        filetype="pdf"
    ) as document:

        for page in document:
            text += page.get_text() + "\n"

    return text


# ------------------------------------
# TEXT CLEANING
# ------------------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ------------------------------------
# EXTRACT SYLLABUS UNITS
# ------------------------------------
def extract_topics(text):
    topics = []

    # Process each line separately
    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Match UNIT I, UNIT 1, MODULE 2, CHAPTER IV, etc.
        if re.search(
            r"\b(unit|module|chapter)\s*[-:]?\s*[ivxlcdm0-9]+\b",
            line,
            re.IGNORECASE
        ):
            topics.append(line)

    # Remove duplicate headings
    return list(dict.fromkeys(topics))


# ------------------------------------
# EXTRACT IMPORTANT KEYWORDS
# ------------------------------------
def extract_keywords(text, top_n=15):
    if not text.strip():
        return []

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=100,
            token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b"
        )

        matrix = vectorizer.fit_transform([text])
        scores = matrix.toarray()[0]
        words = vectorizer.get_feature_names_out()

        ranked = sorted(
            zip(words, scores),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            word for word, score in ranked[:top_n]
            if len(word) > 2
        ]

    except ValueError:
        return []


# ------------------------------------
# GENERATE PRACTICE QUESTIONS
# ------------------------------------
def generate_questions(keywords):
    questions = []

    templates = [
        "Explain the concept of {}.",
        "Discuss the applications of {}.",
        "What are the advantages and limitations of {}?",
        "Describe the working principles of {}.",
        "Compare {} with related concepts.",
        "Explain the importance of {} with suitable examples."
    ]

    for keyword in keywords:
        for template in templates:
            questions.append(template.format(keyword))

    return questions


# ------------------------------------
# FILE UPLOAD
# ------------------------------------
st.markdown(
    '<h2 style="color:#1D4ED8;">1. Upload Your Syllabus</h2>',
    unsafe_allow_html=True
)

syllabus_file = st.file_uploader(
    "Choose your syllabus PDF",
    type=["pdf"],
    key="syllabus"
)


# ------------------------------------
# ANALYZE SYLLABUS
# ------------------------------------
if st.button("Analyze Syllabus", type="primary"):

    if syllabus_file is None:
        st.warning("Please upload your syllabus PDF first.")

    else:
        try:
            with st.spinner("Analyzing your syllabus..."):

                # Extract and clean PDF text
                syllabus_text = extract_text(syllabus_file)
                cleaned_text = clean_text(syllabus_text)

                if not cleaned_text:
                    st.session_state["analysis_done"] = False
                    st.error(
                        "No readable text was found in this PDF. "
                        "It may be a scanned document that requires OCR."
                    )

                else:
                    # Extract units and keywords
                    topics = extract_topics(syllabus_text)
                    keywords = extract_keywords(cleaned_text)

                    # Generate questions
                    questions = generate_questions(keywords)

                    # Save results so they survive Streamlit reruns
                    st.session_state["syllabus_text"] = cleaned_text
                    st.session_state["topics"] = topics
                    st.session_state["keywords"] = keywords
                    st.session_state["questions"] = questions
                    st.session_state["analysis_done"] = True

                    st.success("Syllabus analyzed successfully!")

        except Exception as error:
            st.session_state["analysis_done"] = False
            st.error(f"Unable to process the PDF: {error}")


# ------------------------------------
# DISPLAY SAVED RESULTS
# ------------------------------------
if st.session_state.get("analysis_done", False):

    topics = st.session_state.get("topics", [])
    keywords = st.session_state.get("keywords", [])
    questions = st.session_state.get("questions", [])
    cleaned_text = st.session_state.get("syllabus_text", "")

    # --------------------------------
    # SUMMARY METRICS
    # --------------------------------
    st.markdown(
        '<h2 style="color:#1D4ED8;">📊 Syllabus Overview</h2>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Units Detected", len(topics))

    with col2:
        st.metric("Keywords Found", len(keywords))

    with col3:
        st.metric("Practice Questions", len(questions))

    st.divider()

    # --------------------------------
    # DETECTED UNITS
    # --------------------------------
    with st.expander(
        f"📚 2. Detected Units ({len(topics)})",
        expanded=False
    ):
        if topics:
            for i, topic in enumerate(topics, start=1):
                st.write(f"**{i}.** {topic}")
        else:
            st.info(
                "No unit headings were detected. "
                "Check whether your PDF contains headings like UNIT I or MODULE 1."
            )

    # --------------------------------
    # IMPORTANT KEYWORDS
    # --------------------------------
    with st.expander(
        f"🔑 Important Keywords ({len(keywords)})",
        expanded=False
    ):
        if keywords:
            for i, keyword in enumerate(keywords, start=1):
                st.write(f"**{i}.** {keyword}")
        else:
            st.info("No keywords could be extracted from this syllabus.")

    # --------------------------------
    # PRACTICE QUESTIONS
    # --------------------------------
    st.markdown(
        '<h2 style="color:#1D4ED8;">3. Practice Questions</h2>',
        unsafe_allow_html=True
    )

    st.caption("Click any category to view its questions.")

    if questions:

        sections = {
            "📘 Explain the Concepts": [
                q for q in questions
                if q.startswith("Explain the concept")
            ],

            "💡 Applications": [
                q for q in questions
                if q.startswith("Discuss the applications")
            ],

            "⚖️ Advantages and Limitations": [
                q for q in questions
                if q.startswith("What are the advantages")
            ],

            "⚙️ Working Principles": [
                q for q in questions
                if q.startswith("Describe the working")
            ],

            "🔄 Compare Concepts": [
                q for q in questions
                if q.startswith("Compare")
            ],

            "📝 Importance and Examples": [
                q for q in questions
                if q.startswith("Explain the importance")
            ]
        }

        for section_name, section_questions in sections.items():

            with st.expander(
                f"{section_name} ({len(section_questions)} questions)",
                expanded=False
            ):

                if section_questions:

                    for i, question in enumerate(
                        section_questions, start=1
                    ):
                        st.write(f"**{i}.** {question}")

                    # Download only this category
                    safe_name = re.sub(
                        r"[^a-zA-Z0-9]+",
                        "_",
                        section_name
                    ).strip("_").lower()

                    st.download_button(
                        label="⬇️ Download This Section",
                        data="\n".join(
                            f"{i}. {question}"
                            for i, question in enumerate(
                                section_questions, start=1
                            )
                        ),
                        file_name=f"{safe_name}.txt",
                        mime="text/plain",
                        key=f"download_{safe_name}"
                    )

                else:
                    st.info("No questions available in this section.")

        # Download all questions
        st.download_button(
            label="⬇️ Download All Practice Questions",
            data="\n".join(
                f"{i}. {question}"
                for i, question in enumerate(questions, start=1)
            ),
            file_name="all_practice_questions.txt",
            mime="text/plain",
            key="download_all_questions"
        )

    else:
        st.info("No practice questions could be generated.")

    # --------------------------------
    # EXTRACTED SYLLABUS TEXT
    # --------------------------------
    with st.expander("📄 View Extracted Syllabus Text"):
        st.text_area(
            "Extracted text",
            cleaned_text,
            height=250,
            key="extracted_syllabus_text"
        )

else:
    st.info("Upload your syllabus PDF and click Analyze Syllabus to begin.")
