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
