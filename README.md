# 📄 Know Your Resume

An AI-powered chatbot that allows users to upload a resume (PDF) and interact with it using natural language. The application leverages **LlamaIndex**, **Groq LLM**, and **Hugging Face Embeddings** to provide instant, context-aware responses based on the uploaded resume.

---

## 🚀 Features

- Upload resumes in **PDF** format
- AI-powered question answering based on resume content
- Semantic search using vector embeddings
- Fast responses powered by **Groq Llama 3.3 70B**
- Interactive and responsive Streamlit interface
- Supports conversational queries about skills, education, projects, certifications, and experience

---

## 📸 Screenshot
<p align="center">
  <img src="screenshots/home.png" width="900">
</p>

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Programming Language:** Python
- **LLM:** Groq (Llama 3.3 70B Versatile)
- **Framework:** LlamaIndex
- **Embeddings:** Hugging Face (BAAI/bge-small-en-v1.5)

---

## 📂 Project Structure

```text
Know-Your-Resume/
│── screenshots/
│   └── demo.png
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
└── .env
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Neha7010/Know-Your-Resume.git
cd Know-Your-Resume
```

### 2. Create a virtual environment (Optional)

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

> **Note:** Never upload your `.env` file or API keys to GitHub.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

After running the command, open the local URL displayed in your terminal (typically `http://localhost:8501`).

---

## 💡 How to Use

1. Launch the application.
2. Upload a resume in PDF format.
3. Click **Index PDF**.
4. Ask questions such as:

- Summarize the resume.
- What technical skills are mentioned?
- List the projects.
- What certifications does the candidate have?
- What programming languages are included?
- What education details are available?

---

## 📌 Future Enhancements

- ATS Resume Score Analysis
- Resume Improvement Suggestions
- Interview Question Generation
- Support for Multiple PDF Uploads
- Export Chat History
- Multi-language Support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 👩‍💻 Author

**Neha Kurian**

- GitHub: https://github.com/Neha7010
- LinkedIn: https://www.linkedin.com/in/neha-kurian-258221296/

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
