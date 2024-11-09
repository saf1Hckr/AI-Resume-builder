from openai import OpenAI
import os
from dotenv import load_dotenv


#Check your .env file and place your openai key there
load_dotenv()
client = OpenAI(
     api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_response(user_input: str) -> str:
    message: str = user_input.lower()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
         messages=[{"role": "system", "content":'You are to make a Summary of each of my below message script of just 3-5 sentencese. After that, THEN ENSURE YOU LIST ALL THE TECHNOLOGY USED IF THERES ANY. just list them no need to explain them'},
                   {"role": "user", "content": message}]

        )
   # print(response) print everything thats send back from open ai
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip() 





