import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai

openai.api_key = st.secrets["mykey"]

# Replace with your embedding model
model = "text-embedding-ada-002"

# Load your dataset
df = pd.read_csv('qa_dataset_with_embeddings.csv')

# Function to get embedding
def get_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    embedding = response['data'][0]['embedding']
    return np.array(embedding).reshape(1, -1)

def find_best_answer(user_question):
    # Get embedding for the user's question
    user_question_embedding = get_embedding(user_question)

    # Calculate cosine similarities for all questions in the dataset
    df['Similarity'] = df['Question_Embedding'].apply(lambda x: cosine_similarity(x, user_question_embedding))

    # Find the most similar question and get its corresponding answer
    most_similar_index = df['Similarity'].idxmax()
    max_similarity = df['Similarity'].max()

    # Set a similarity threshold to determine if a question is relevant enough
    similarity_threshold = 0.6  # You can adjust this value

    if max_similarity >= similarity_threshold:
        best_answer = df.loc[most_similar_index, 'Answer']
        return best_answer
    else:
        return "I apologize, but I don't have information on that topic yet. Could you please ask other questions?"

def main():
    st.title("Health Question Answering")

    user_question = st.text_input("Ask your health question")
    if st.button("Submit"):
        if user_question:
            best_answer = find_best_answer(user_question)
            st.write(best_answer)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()