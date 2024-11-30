from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve OpenAI API key from the environment variables
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

os.environ['OPENAI_API_KEY'] = api_key

class AIAssistantFactory:
    @staticmethod
    def create_llm(model_name):
        return OpenAI()

    @staticmethod
    def api_call_with_delay(client, prompt, model="gpt-4o-mini"):
        time.sleep(5)  # Reduced delay to 5 seconds
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content
