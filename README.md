# 🚀 Smart Search System for Analytics Vidhya Courses 🔍

## Project Link
[[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/AmritSbisht/Analytics_Vidhya_Search_bot)]

## 📌 Project Overview
This project implements a smart search system for Analytics Vidhya courses, utilizing web scraping, embeddings, and Large Language Models (LLMs) to provide tailored course recommendations. It integrates Retrieval-Augmented Generation (RAG) for enhanced query relevance and detailed analysis.

## 📂 Repository Structure
```
course_search_project/
|-── data/
|   └── detailed_courses.csv
|── scraper/
│   └── course_scraper.py
│── app.py
│── requirements.txt
└── README.md
```
### 📌 Components:
1. **📊 Data:** Contains `detailed_courses.csv`, storing structured course details.
2. **🛠️ Scraper:** Includes `course_scraper.py` for web scraping and data extraction.
3. **💻 App:** A Streamlit-based interface (`app.py`) for course search and recommendation.
4. **📜 Dependencies:** Listed in `requirements.txt`.

## 🕵️‍♂️ Scraping Methodology
### 🎯 Objective
Extract comprehensive course information, including:
- 📌 Title
- 🔗 URL
- 📝 Brief Description
- 📈 Level
- ⏳ Duration
- 📚 Curriculum
- 🎯 Target Audience and Benefits
- ❓ FAQs

### ⚙️ Implementation
1. **🔍 Course Listing Extraction:**
   - Visits paginated course listing pages.
   - Filters free courses using the "Free" price tag.
   - Captures the course title, link, and page number.
2. **📖 Detailed Course Scraping:**
   - Extracts course details such as duration, rating, curriculum, FAQs, and trainer information.
   - Uses BeautifulSoup for HTML parsing.
   - Implements respectful request delays.
3. **💾 Data Saving:**
   - Stores structured data in `detailed_courses.csv`, serving as the data source for recommendations.

## 🧠 Embedding Model Selection
### 🎯 Objective
Convert course information into numerical vectors for efficient similarity searches.

### 🤖 Model Used
- **Google Generative AI Embeddings**
  - **Model:** `models/embedding-001`
  - **✨ Features:** High-quality semantic representations.
  - **🔗 Integration:** Works seamlessly with FAISS for vector similarity searches.

### 🔧 Configuration
- API-based access via `langchain_google_genai`.
- **Why this model?**
  - ✅ Superior contextual understanding.
  - ✅ Efficient vector storage and retrieval.

## 📝 LLM Selection and Methodology
### 🎯 Objective
Generate human-like, detailed course recommendations.

### 🤖 Model Used
- **Google Generative AI LLM**
  - **Model:** `gemini-pro`
  - **⚙️ Configuration:**
    - Temperature: 0.1
    - Top-p: 0.8, Top-k: 40
    - Max output tokens: 2048

### 🎯 Prompt Engineering
The LLM is guided to:
1. Analyze user queries.
2. Recommend courses based on relevance, features, and audience suitability.
3. Suggest learning paths.

#### 💡 Example Prompt:
```
Act as an experienced course advisor analyzing courses for a student interested in: "{query}".
Analyze these relevant courses:
{relevant_chunks}
Provide a detailed analysis that includes:
1. Query Analysis.
2. Course Recommendations (with reasons and benefits).
3. Best Match Identification.
4. Learning Path Suggestions.
```

## 🔄 Retrieval-Augmented Generation (RAG) Integration
### 🎯 Objective
Enhance responses by combining vector-based retrieval with generative AI.

### 🛠️ Methodology
1. **🔍 Vector Search:** Queries are embedded and matched with stored vectors via FAISS.
2. **🧩 Contextual Analysis:** Relevant courses are structured into a prompt and sent to the LLM.
3. **📝 Response Generation:** The system combines retrieved content with generative insights for tailored recommendations.

## 🔄 System Workflow
1. **📂 Data Loading:** Reads `detailed_courses.csv` and processes text for embedding.
2. **🔍 Vector Store Initialization:** Embeds text and stores it in FAISS.
3. **🎯 Course Search:** Retrieves top-k similar embeddings.
4. **📝 Response Generation:** Passes query and relevant course data to the LLM for recommendations.

## 🚀 How to Run the Project
### ⚙️ Prerequisites
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set up API keys for Google Generative AI models.
3. Ensure `detailed_courses.csv` is present in the `data/` directory.

### ▶️ Running the Application
```sh
streamlit run app.py
```

## 🎯 Conclusion
This system integrates web scraping, semantic search, and LLM capabilities to deliver personalized course recommendations. By leveraging high-quality embeddings and generative models, it ensures relevance, depth, and user satisfaction.

## 🔗 Project Link
[[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/AmritSbisht/Analytics_Vidhya_Search_bot)]
