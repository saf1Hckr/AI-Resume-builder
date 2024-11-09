from pymilvus import MilvusClient
import numpy as np



# Initialize Milvus Client
client = MilvusClient("TraingData.db")
# collection_name = "Faiss_App3"

def get_collection_name(user_id):
    """Helper function to get collection name from user ID."""
    return f"_{user_id}"

def create_milvus_collection(User_id, dimension=1536):
    
    collection_name = get_collection_name(User_id)
    if not client.has_collection(collection_name=collection_name):
        # Create the collection with the dimension specified and no specific fields
        client.create_collection(
            collection_name=collection_name,
            dimension=dimension,
        )
        print ("just created collection: " + collection_name)
    else:
        print("collection name: " +  User_id)

def insert_into_milvus(data, User_Id):

    collection_name = get_collection_name(User_Id)
    # Insert the embeddings as records directly into Milvus
    client.insert(
        collection_name=collection_name,
        data=data  # Directly pass the list of dictionaries
    )
    # After insertion, print the number of entities in the collection
    print(f"Inserted {len(data)} records into the collection '{collection_name}'.")

    
def query_milvus(query_embedding, User_id, limit=10):
    collection_name = get_collection_name(User_id)

    # Ensure the query_embedding is a list of floats and wrap in a list of lists
    if not isinstance(query_embedding, np.ndarray):
        query_embedding = np.array(query_embedding, dtype=float)
    query_embedding = [query_embedding.tolist()]  # Wrap in a list

    # Check if the collection exists before querying
    if not client.has_collection(collection_name=collection_name):
        create_milvus_collection(User_id, dimension=1536)

    # Perform the search query
    try:

        
        return client.search(
            collection_name=collection_name,
            data=query_embedding,
            limit=limit,
            output_fields=["title","text", "subject", "time", "distance"]
        )
    except Exception as e:
        print(f"Failed to search collection: {collection_name}")
        print(f"Error: {e}")
        return None
