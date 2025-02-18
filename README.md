# Cocktail Advisor Chat

This project implements a chatbot for cocktail recommendations using a Retrieval-Augmented Generation (RAG) approach. It uses FastAPI for the REST API, FAISS for vector search, and a free Hugging Face model (distilgpt2) for generating responses.

## Features

- **Cocktail Knowledge Base:**  
  Answer queries such as:
  - "What are the 5 cocktails containing lemon?"
  - "What are the 5 non-alcoholic cocktails containing sugar?"
  - "What are my favorite ingredients?"
  
- **Cocktail Advisor:**  
  Provide recommendations like:
  - "Recommend 5 cocktails that contain my favorite ingredients."
  - "Recommend a cocktail similar to 'Hot Creamy Bush'."

- **User Preferences:**  
  The chatbot detects when the user shares their favorite ingredients or cocktails (e.g., "My favorite ingredients: rum, lime, mint") and saves this information for future recommendations.

## Technologies Used

- **Backend:** FastAPI, Python
- **LLM:** Hugging Face's distilgpt2 model
- **Vector Database:** FAISS with SentenceTransformers (using the "all-MiniLM-L6-v2" model)
- **Frontend:** A simple HTML/JavaScript chat interface enhanced with Bootstrap for a modern, intuitive design

## How to Run Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Kyivnik/cocktail-advisor-chat
   cd cocktail-advisor
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Place the dataset:**

   Download `final_cocktails.csv` from [Kaggle](https://www.kaggle.com/datasets/aadyasingh55/cocktails) and place it in the `data/` folder.

4. **Start the server:**

   ```bash
   uvicorn api.main:app --reload
   ```

5. **Open the chat interface:**

   Navigate to [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html) in your browser.

## Known Issues and Future Improvements

While the system is fully functional, I encountered some challenges with text processing and generating intuitive responses. The answers, although complete, can sometimes be a bit verbose and less intuitive than desired. I believe that with further development—especially by splitting responsibilities within the project—these aspects can be significantly improved.

I am confident in my ability to address these challenges and look forward to further refining the application. Constructive feedback and collaborative efforts would help take this project to the next level.

## Conclusion

This project showcases my skills in Python, FastAPI, and modern NLP/vector search technologies. I take pride in delivering a complete solution and am enthusiastic about continuing to enhance its capabilities. I welcome the opportunity to collaborate and contribute further, confident in my potential to bring substantial value to any team.
