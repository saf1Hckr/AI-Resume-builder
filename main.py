from OpenAi_embedding import get_openai_embedding
from jobposting import jobposting
from milvus_handler import create_milvus_collection, insert_into_milvus, query_milvus
from OpenAi_response import getAiresponse
from milvus_handler_jobs import create_milvus_collection2, insert_into_milvus2, query_milvus2
from resumeUpload import getFilepath2

# Define user ID and sample job postings for testing
user_id = "user123"
id_counter = 1  # Initial ID counter

sample_jobs= jobposting()

# Create Milvus collection if not already present
create_milvus_collection(user_id)
create_milvus_collection2(user_id)

# # Prepare embeddings for insertion
# embedding_data = []
# for job in sample_jobs:
#     embedding = get_openai_embedding(job['description'])
#     if embedding is not None:
#         embedding_data.append({
#             "id": id_counter,
#             "vector": embedding.tolist(),  # Convert ndarray to list
#             "title": job['title'],  # Include title in the insertion data
#             "text": job['description'],  # Include description
#             "subject": job['link'],  # Include job link
#             "time": job['time']  # Include posting time
#         })
#         id_counter += 1  # Increment the ID for the next entry
#     else:
#         print("Text exceeds the maximum token limit; embedding was not generated.")

# Insert embeddings into Milvus
# if embedding_data:
#     insert_into_milvus2(embedding_data, user_id)

# Perform a query using one of the job descriptions 
job_description = f"""
    Job Title: Computer Science Specialist
    
    Description:
    We are looking for a motivated and skilled Computer Science Specialist to join our team. This role involves contributing to the development, analysis, and maintenance of various technical projects, focusing on implementing state-of-the-art AI and software development practices. The candidate should be experienced in coding, data structures, algorithms, and integrating AI solutions to solve complex problems. They will work closely with a cross-functional team, leveraging machine learning models, building scalable systems, and ensuring software solutions align with business goals.
    
    Key Responsibilities:
    - Design and develop software systems to enhance project efficiency.
    - Collaborate with AI experts to integrate machine learning models.
    - Maintain and optimize existing codebases for performance improvements.
    - Create technical documentation and contribute to knowledge sharing.
    - Ensure software applications are secure, scalable, and robust.
    - Work with cloud technologies and databases for deploying AI models.
    - Analyze user needs and create solutions that align with project requirements.
    
    Qualifications:
    - Bachelor’s or Master’s degree in Computer Science or related field.
    - Proficiency in programming languages such as Python, Java, C++, or JavaScript.
    - Experience with machine learning frameworks and libraries (e.g., TensorFlow, PyTorch).
    - Knowledge of vector databases (e.g., Milvus) and embedding technologies.
    - Strong problem-solving and analytical skills.
    - Effective communication and teamwork abilities.
    
    Location: [Specify the area]

    If you have a passion for technology and an innovative approach to problem-solving, we encourage you to apply for this exciting opportunity to advance your career in the computer science field.
    """
getAiresponse(job_description,user_id)

query_text = getFilepath2('Resume Upload') 
print (query_text)
query_embedding = get_openai_embedding(query_text)

if query_embedding is not None:
    results = query_milvus2(query_embedding, user_id)
    if results:
        for result in results:
            for match in result:
                # Access 'title', 'text', 'subject', and 'posting_time' within the 'entity' dictionary
                entity = match['entity']
               

                print(f"Matched job title: {entity.get('title')}")
                print(f"Matched job description: {entity.get('text')}")
                print(f"Job link: {entity.get('subject')}")
                print(f"Posting time: {entity.get('time')}")
                print(f"Distance: {match.get('distance')}")
                print("-" * 50)
    else:
        print("No results found or an error occurred.")
else:
    print("Query text exceeds the maximum token limit; embedding was not generated.")
