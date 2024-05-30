# Usage
# All travel articles should be stored in the data/travel_articles folder

# from unstructured_rag import main
# user_request = "I want to travel to a Greek Island that is famous this season for eating good food. Wbich one would you recommend to me?"
# main(user_request=user_request)

import openai
from openai import AzureOpenAI
import os
from IPython.display import display, Markdown, HTML
import pandas as pd
import numpy as np
import tiktoken
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv 
import pickle 
load_dotenv();

# Model
MODEL = os.environ.get("OPENAI_API_DEPLOYMENT", "gpt-4")
# MODEL = "gpt-35-turbo"  # Uncomment if token rate is too high

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
)

embedding_model = SentenceTransformer("all-mpnet-base-v2")

def get_list_from_pkl(path_to_file: str) -> List[str]:
    """
    Function to get a list of strings from a pkl file.
    """
    content = []
    with open(path_to_file, "rb") as f:
        content = pickle.load(f)
    
    return content

def distance_between_vector_and_vectors(
    vector: np.ndarray, vectors_array: np.ndarray
    ) -> np.ndarray:
    """
    Calculate the cosine similarities between a single vector and an array of vectors.

    Args:
        vector: A single vector
        vectors_array: An array of vectors
    
    Returns:
        An array of cosine similarities
    """
    dot_products = np.dot(vectors_array, vector)

    # Calculate the magnitudes of all vectors in vectors_array
    magnitudes = np.sqrt(np.sum(np.square(vectors_array), axis=1))

    # Calculate the magnitude of vector
    magnitude_1 = np.linalg.norm(vector)

    # Calculate the cosine similarities between vector and all vectors in vectors_array
    similarities = dot_products / (magnitude_1 * magnitudes)

    return similarities


def get_pieces_of_interest(question: str, embeddings: list, travel_articles: list, k: int = 3) -> List[str]:
    """Function to get the pieces of interest for a question.
    
    Args:
        question: The question to ask the model
        k: The number of pieces of interest to find
    
    Returns:
        The pieces of interest
    """
    question_embedding = embedding_model.encode(question, show_progress_bar=True)

    distances = distance_between_vector_and_vectors(
        vector=question_embedding,
        vectors_array=embeddings
    )

    idx_of_interest = list((-distances).argsort()[:k])
    pieces_of_interest = [travel_articles[i] for i in idx_of_interest]

    return pieces_of_interest


def get_augmented_prompt(
        question: str,
        pieces_of_interest: List[str],
        context_instruction: str,
    ) -> str:
    """Function to build the augmented prompt.
    
    Args:
        question: The question to ask the model
        pieces_of_interest: The pieces of interest
        context_instruction: The context instruction
    
    Returns:
        The augmented prompt
    """
    augmented_prompt = f"{context_instruction} \n\n Question: {question} \n\n The travel articles follow below: \n\n"

    for piece in pieces_of_interest:
        augmented_prompt += piece

    return augmented_prompt

def ask_question(
        prompt: List[Dict[str, str]],
        model: str = MODEL
    ) -> openai.types.chat.chat_completion.ChatCompletion:
    """Function to ask a question to the GPT model using the Azure OpenAI API.
    
    Args:
        prompt: The prompt to send to the GPT model
        model: The model to use

    Returns:
        The response from the GPT model
    """

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=0.7,
        max_tokens=1500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    
    return response

def main(user_request: str) -> str:
    """Main function for unstructured RAG."""

    path_travel_articles = "./data/travel_articles.pkl"
    path_embeddings = "./data/embeddings.pkl"
    embeddings = get_list_from_pkl(path_embeddings)
    travel_articles = get_list_from_pkl(path_travel_articles)

    k = 1

    pieces_of_interest = get_pieces_of_interest(
        question=user_request, embeddings=embeddings, travel_articles=travel_articles,
        k=k
    )

    character = "You are a seasoned travel agent with the primary goal to help users looking to plan a vacation in Greece. You write in a friendly yet professional tone."

    context_instruction = 'Use the below travel articles about Greek Islands from the current travel season to answer \
    the subsequent question. If the answer cannot be found in the articles, write "I could \
    not find an answer."'
    augmented_prompt = get_augmented_prompt(
            question=user_request,
            pieces_of_interest=pieces_of_interest,
            context_instruction=context_instruction,
    )

    prompt = [
        {
            "role": "system",
            "content": character
        },
        {
            "role": "user",
            "content": augmented_prompt
        },
    ]

    response = ask_question(
        prompt=prompt,
        model=MODEL
    )

    answer = response.choices[0].message.content

    return answer