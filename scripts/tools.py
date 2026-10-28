import json
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


def get_weather(location: str) -> dict[str, str | int | bool]:
    """Return simulated weather data to demonstrate function calling."""
    return {
        "location": location,
        "temperature": 18,
        "unit": "C",
        "simulated": True,
    }


tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Return simulated weather data for a location; not real current weather.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def main() -> None:
    client = OpenAI(api_key=load_configuration())
    response = client.responses.create(
        model="gpt-6-astra",
        input="Demonstrate get_weather for Paris. State clearly that its data is simulated.",
        tools=tools,
        tool_choice={"type": "function", "name": "get_weather"},
    )

    tool_outputs = []
    for item in response.output:
        if item.type != "function_call":
            continue
        if item.name != "get_weather":
            raise ValueError(f"Función desconocida: {item.name}")

        arguments = json.loads(item.arguments)
        weather = get_weather(location=arguments["location"])
        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(weather),
            }
        )

    if not tool_outputs:
        raise RuntimeError("El modelo no devolvió una llamada a get_weather.")

    final_response = client.responses.create(
        model="gpt-6-astra",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
        tool_choice="none",
    )
    print(final_response.output_text)


if __name__ == "__main__":
    main()
