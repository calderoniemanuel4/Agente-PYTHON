import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key

def load_configuration() -> None:
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configurala en .env o en las variables del entorno."
        )
    set_default_openai_key(api_key)
load_configuration()
###  AQUI COMIENZA EL CODIGO PARA PROBAR ###


from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text.",
    output_type=CalendarEvent,
)


async def main() -> None:
    result = await Runner.run(
        agent,
        "Dinner with Priya and Sam on Friday.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())