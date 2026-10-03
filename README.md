# 📚 Exam Question Predictor

An interactive web application built with Python and Streamlit that analyzes a syllabus PDF, extracts topics and keywords, and generates practice questions to help students prepare for exams.

## ✨ Features

* 📄 Upload a syllabus in PDF format.
* 📚 Detect unit and module headings.
* 🔑 Extract important keywords from the syllabus.
* 📝 Generate practice questions based on extracted keywords.
* 📂 View questions in expandable, category-wise sections.
* ⬇️ Download individual question sections or all questions.
* 🎨 Simple and user-friendly interface.

## 🛠️ Technologies Used

* Python
* Streamlit
* PyMuPDF
* Scikit-learn
* TF-IDF Vectorization

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd exam-question-predictor
```

### 3. Create a virtual environment (optional)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

##  How to Use

1. Open the application.
2. Upload your syllabus PDF.
3. Click **Analyze Syllabus**.
4. Expand the Detected Units and Important Keywords sections.
5. Explore practice questions by category.
6. Download the questions for revision.

## Project Note

The application generates practice questions from keywords extracted from the syllabus. These are suggested practice questions, not guaranteed predictions of questions that will appear in an examination.

## Future Improvements

* More accurate topic and keyword extraction.
* AI-powered question generation.
* Support for different question formats and difficulty levels.
* Unit-wise question generation.
* Previous-year question paper analysis.

## Author

Sejal Gayathri

Built as a learning project to explore Python, natural language processing techniques, and Streamlit web application development.
