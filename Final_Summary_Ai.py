from openai import OpenAI
import os
from dotenv import load_dotenv


#Check your .env file and place your openai key there
load_dotenv()
client = OpenAI(
     api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_Finalresponse(user_input: str) -> str:
    message: str = user_input.lower()

    response = client.chat.completions.create(
        model="gpt-4o",
         messages=[{"role": "system", "content":'Read the text carefully and make a descript detailed summary on the content below. finaly just List atmost the 6 most important technology base on the below summary.'},
                   {"role": "user", "content": message}]

        )
   # print(response) print everything thats send back from open ai
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip() 





