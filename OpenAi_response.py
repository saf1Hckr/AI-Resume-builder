import numpy as np
from OpenAi_embedding import get_openai_embedding, client as openai_client
from Summary_Ai import get_response
from milvus_handler import query_milvus, client as milvus_client

def getAiresponse(query_text, User_id):
    print("We just got the embedding")
    generated_response = "Sorry, I could not find any relevant information to respond to your query."  # Default response
    
    # Get the embedding for the query text
    query_embedding = get_openai_embedding(query_text)
    

    personal_info = (
    "Name: John Smith\n"
    "Phone: (555) 123-4567\n"
    "Email: john.smith@example.com\n"
    "LinkedIn: linkedin.com/in/johnsmith\n"
    "Address: 123 Main Street, Apt 4B, New York, NY 10001\n"
    "Portfolio: www.johnsmithportfolio.com\n"
    "Graduation data: May 2025"
  
)

 
    if query_embedding is not None:
            results = query_milvus(query_embedding, User_id)
            if results:
                context_list = []  # List to collect context details
                for result in results:
                    for match in result:
                        # Access 'title', 'text', and 'subject' within the 'entity' dictionary
                        entity = match['entity']
                        title = entity.get('title')
                        description = entity.get('text')
                        link = entity.get('subject')
                        distance = match.get('distance')

                        # Collect each job's details into a formatted string
                        if title and description and link:
                            job_details = (
                                f"Title: {title}\n"
                                f"Description: {description}\n"
                                f"Link: {link}\n"
                                f"Distance: {distance:.2f}\n"
                                "-" * 50
                            )
                            context_list.append(job_details)

                # Combine the job details into a single context string
                if context_list:
                    full_context = "\n\n".join(context_list)
                    print("Context to be fed to OpenAI:")
                  #  print(full_context)  # Optional: for debugging

                    # Generate a response using OpenAI's language model
                    response = openai_client.chat.completions.create(
                        model="gpt-4o",  # Or any other model you prefer
                        messages=[
                            {"role": "system", "content": "You are a resume builder, You are to use the context given which is a summary on my project/projects/resumes/experience and build a resume for me and make my resume to best match the job description base on my projects/resume/experience"},
                            {"role":"user", "content": f"This is a summary of the job description: {get_response(query_text)}"},
                            {"role": "user", "content": f"Here is data, use this data to add relevant stuff to my resume: {full_context}."},
                            {"role": "user", "content": f"Here is my personal information: {personal_info}" },
                            {"role": "user", "content": f"Here is a resume Template i want you to follow, follow this exactly this down to the markdown. Must have minimum of 3 bullet points for each project and job experience: {gettemplate()}."},
                            {"role": "user", "content": f"Based on the above data, please make a resume for me."}
                        ]
                    )

                    # Extract and store the generated response
                    generated_response = response.choices[0].message.content.strip()
                    print("Generated response:")
                    print(generated_response)
                else:
                    print("No relevant data found in the Milvus collection.")
            else:
                print("No relevant data found in the Milvus collection.")
    else:
            print("Query text exceeds the maximum token limit; embedding was not generated.")

        # else:
        #     print("Query text exceeds token limit.")
    
    return generated_response

def gettemplate():
    template = (
        "# [Your Name]\n"
        "**[Your City, State]** • [Your Email] • [Your Phone Number] • [Your LinkedIn URL] • [Your Portfolio URL]\n"
        "\n"
        "## Education\n"
        "**[Institution Name], [Degree (e.g., Bachelor of Science in Computer Science)]**\n"
        "[City, State] — *Graduation [Month Year]*\n"
        "- Relevant Coursework: [Course Name 1, Course Name 2, Course Name 3, etc.]\n"
        "\n"
        "## Skills\n"
        "- **Languages**: [e.g., Java, C++, Python, etc.]\n"
        "- **Tools and Frameworks**: [e.g., Node.js, React, Django, AWS, etc.]\n"
        "- **Specialties**: [e.g., Artificial Intelligence, Web Development, Full Stack Development, etc.]\n"
        "\n"
        "## Work Experience\n"
        "**[Job Title], [Company Name]**\n"
        "[City, State] — *[Start Date] – [End Date]*\n"
        "- [Key responsibility or achievement #1]\n"
        "- [Key responsibility or achievement #2]\n"
        "- [Key responsibility or achievement #3]\n"
        "\n"
        "**[Job Title], [Company Name]**\n"
        "[City, State] — *[Start Date] – [End Date]*\n"
        "- [Key responsibility or achievement #1]\n"
        "- [Key responsibility or achievement #2]\n"
        "- [Key responsibility or achievement #3]\n"
        "\n"
        "## Leadership & Professional Development\n"
        "**[Role], [Organization Name]**\n"
        "[City, State] — *[Start Date] – Present*\n"
        "- [Key contribution or project]\n"
        "- [Impact achieved]\n"
        "\n"
        "## Projects\n"
        "**[Project Name]** (*Technology Stack*) — [Link to Demo/GitHub]\n"
        "- [Brief description of the project, your role, and the impact.]\n"
        "\n"
        "**[Project Name]** (*Technology Stack*) — [Link to Demo/GitHub]\n"
        "- [Brief description of the project, your role, and the impact.]\n"
        "\n"
        "## Certifications\n"
        "- **[Certification Name]** — [Issuing Organization], *[Year]*\n"
        "\n"
        "## Awards\n"
        "- **[Award Name]** — [Awarding Organization], *[Year]*\n"
    )
    return template

