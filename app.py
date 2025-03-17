import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import tempfile

# Load environment variables
load_dotenv()

class CourseSearchSystem:
    def __init__(self):
        """
        Initialize the course search system with Google's Generative AI
        """
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.generation_config = {
            'temperature': 0.1,  # Lower temperature for more consistent outputs
            'top_p': 0.8,       # Reasonable top_p value for focused sampling
            'top_k': 40,        # Standard top_k value
            'max_output_tokens': 2048,  # Ensure sufficient length for detailed analysis
        }
        self.generation_model = genai.GenerativeModel('gemini-pro',
                                                    generation_config=self.generation_config)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = None
        self.course_data = []

    def process_course(self, row):
        """
        Process a single course row into a formatted string
        """
        return f"""
        TITLE: {row['Title']}
        BRIEF: {row['Brief']}
        LEVEL: {row['Level']}
        DURATION: {row['Duration']}
        DESCRIPTION: {row['Description']}
        URL: {row['Link']}
        CURRICULUM: {row['Curriculum']}
        TARGET AUDIENCE AND BENEFITS: {row['What should enroll & takeaway']}
        """

    def create_vector_store(self, df):
        """
        Create vector store from course data
        """
        texts = []
        for _, row in df.iterrows():
            doc = self.process_course(row)
            texts.append(doc)
            self.course_data.append({
                'title': row['Title'],
                'brief': row['Brief'],
                'level': row['Level'],
                'duration': row['Duration'],
                'url': row['Link'],
                'curriculum': row['Curriculum'],
                'target_audience': row['What should enroll & takeaway']
            })
        
        self.vector_store = FAISS.from_texts(texts, self.embeddings)

    def search_courses(self, query, k=3):
        """
        Search for relevant courses based on query
        """
        try:
            if not self.vector_store:
                return "Error: Search index not initialized.", []

            similar_docs = self.vector_store.similarity_search(query, k=k)
            
            relevant_courses = []
            relevant_chunks = []
            
            for doc in similar_docs:
                doc_content = doc.page_content
                try:
                    idx = next(i for i, course in enumerate(self.course_data) 
                             if course['title'] in doc_content)
                    relevant_courses.append(self.course_data[idx])
                    relevant_chunks.append(doc_content)
                except StopIteration:
                    continue

            if not relevant_courses:
                return "No matching courses found for your query.", []
            
            # Enhanced structured prompt for more consistent results
            context = f"""
            Act as an experienced course advisor analyzing courses for a student interested in: "{query}"

            Based on their interest, analyze these relevant courses:
            {relevant_chunks}

            Provide a detailed analysis that includes:
            1. Query Analysis: What specific learning needs or interests are indicated by this query
            2. Course Recommendations: For each relevant course:
               - Explain why it matches the student's needs
               - Highlight key features and benefits
               - Specify who would benefit most from this course
            3. Best Match: Identify the most suitable course and explain
            4. Learning Path: Suggest how the student might progress through these courses if relevant

            Be specific in your analysis, mentioning course titles and concrete features.
            Focus on how each course addresses the student's learning objectives.

            """
            
            try:
                response = self.generation_model.generate_content(context)
                return response.text, relevant_courses
            except Exception as e:
                return f"Error generating course analysis: {str(e)}", relevant_courses
                
        except Exception as e:
            return f"Error during course search: {str(e)}", []

def main():
    """
    Main function to run the Streamlit application
    """
    st.title("🎓 Analytics Vidhya Course Search Assistant")
    st.write("Find the perfect free course for your learning journey with AI-powered recommendations.")
    
    @st.cache_resource
    def initialize_search_system():
        return CourseSearchSystem()
    
    @st.cache_data
    def load_and_process_data():
        csv_path = r"data/detailed_courses.csv"
        try:
            df = pd.read_csv(csv_path)
            return df
        except FileNotFoundError:
            st.error(f"Could not find the file: {csv_path}")
            st.info("Please ensure the CSV file path is correct.")
            return None

    search_system = initialize_search_system()
    df = load_and_process_data()
    
    if df is not None:
        if 'index_built' not in st.session_state:
            with st.spinner("Building search index... This may take a moment."):
                search_system.create_vector_store(df)
                st.session_state.index_built = True

        with st.form(key='search_form'):
            query = st.text_input("🔍 What would you like to learn?", 
                                placeholder="Example: machine learning for beginners")
            search_button = st.form_submit_button("Search Courses", use_container_width=True)

        if query and search_button:
            with st.spinner("Analyzing courses for you..."):
                response, courses = search_system.search_courses(query)
                
                if courses:
                    st.write("### 📊 Course Analysis")
                    st.write(response)
                    
                    st.write("### 📚 Recommended Courses")
                    for course in courses:
                        with st.expander(f"📘 {course['title']}", expanded=True):
                            cols = st.columns([1, 1])
                            with cols[0]:
                                st.write(f"**Level:** {course['level']}")
                                st.write(f"**Duration:** {course['duration']}")
                            
                            with cols[1]:
                                st.markdown(f"[**Enroll Now** 🚀]({course['url']})")
                            
                            st.write("**Overview:**")
                            st.write(course['brief'])
                            
                else:
                    st.warning("No courses found matching your query. Please try different search terms.")

if __name__ == "__main__":
    main()