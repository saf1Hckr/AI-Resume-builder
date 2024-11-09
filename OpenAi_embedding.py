import tiktoken
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_openai_embedding(text, max_tokens=8192):
    # Use an explicit encoding method
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Replace with the encoding relevant to your model

    tokens = tokenizer.encode(text)

    if len(tokens) > max_tokens:
        return None  # Skip embedding if it exceeds the token limit

    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"  # Replace with a valid OpenAI embedding model
    )

    embedding = response.data[0].embedding
    return np.array(embedding, dtype='float32')


# if __name__ == "__main__":
#     # Sample text to embed
#     sample_text = "Artificial Intelligence is revolutionizing many industries and shaping the future."

#     # Get the embedding for the sample text
#     embedding = get_openai_embedding(sample_text)

#     if embedding is not None:
#         print("Embedding generated successfully!")
#         print("Embedding vector (first 10 values):", embedding[:10])  # Print the first 10 values of the embedding
#     else:
#         print("Text exceeds the maximum token limit; embedding was not generated.")
