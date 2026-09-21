import os

from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


MODELOS = {
    "gemini": {
        "provider": "google",
        "model": "gemini-2.5-flash",
        "output": "./resultados/gemini"
    },
    "llama": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "output": "./resultados/llama"
    },
    "gpt": {
        "provider": "groq",
        "model": "openai/gpt-oss-20b",
        "output": "./resultados/gpt"
    }
}


def gerar_resposta_modelo(prompt, modelo):

    config = MODELOS[modelo]

    if config["provider"] == "google":

        model = genai.GenerativeModel(
            config["model"]
        )

        resposta = model.generate_content(prompt)

        return resposta.text

    elif config["provider"] == "groq":

        resposta = groq_client.chat.completions.create(
            model=config["model"],
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return resposta.choices[0].message.content

    else:

        raise ValueError(
            f"Provider '{config['provider']}' não suportado."
        )