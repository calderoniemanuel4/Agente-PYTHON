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

def main() -> None:
    client = OpenAI(api_key=load_configuration())
    response = client.responses.create(
        model="gpt-6-astra",
        input="Write a short bedtime story about a unicorn in spanish language",
    )

    print(response.output_text)


#   BLOQUE PARA CONSULTAR TOKENS   #


    if response.usage is None:
        print("Uso de tokens no disponible para esta respuesta.")
    else:
        print(
            f"Tokens — entrada: {response.usage.input_tokens}, "
            f"salida: {response.usage.output_tokens}, "
            f"total: {response.usage.total_tokens}"
        )


if __name__ == "__main__":
    main()
