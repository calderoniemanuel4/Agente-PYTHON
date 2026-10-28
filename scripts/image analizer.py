import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def load_configuration() -> str:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configurala en .env o en las variables del entorno."
        )
    return api_key

client = OpenAI(api_key=load_configuration())

response = client.responses.create(
    model="gpt-6-astra",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "What teams are playing in this image?",
                },
                {
                    "type": "input_image",
                    "image_url": "https://api.nga.gov/iiif/a2e6da57-3cd1-4235-b20e-95dcaefed6c8/full/!800,800/0/default.jpg",
                },
            ],
        }
    ],
)

print(response.output_text)
if response.usage is None:
    print("Uso de tokens no disponible para esta respuesta.")
else:
    print(
        f"Tokens — entrada: {response.usage.input_tokens}, "
        f"salida: {response.usage.output_tokens}, "
        f"total: {response.usage.total_tokens}"
    )
