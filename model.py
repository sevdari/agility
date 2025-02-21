import os
from dotenv import load_dotenv
from openai import OpenAI

# Create a model class from which objects can be created to interact with the model.
# Model objects allows for easy switching between different models.

class Model:
    def __init__(self, model_name, system_prompt, temperature=0.7):
        self.model_name = model_name
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = system_prompt
        self.temperature = temperature

        self.context_history = []


    def prompt(self, system_prompt, user_prompt, temperature=None, update_temperature=False, update_context=True):
        if temperature is None:
            temperature = self.temperature
        if update_temperature:
            self.temperature = temperature

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )

        context = [
            {"user_prompt" : user_prompt},
            {"assistant_response" : response.choices[0].message.content},
        ]

        if update_context:
            self.context_history.append(context)

        return response.choices[0].message.content