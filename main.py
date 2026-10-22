import asyncio
import os
from pathlib import Path

from agents import Agent, Runner
from dotenv import load_dotenv

agent = Agent(
    name="History tutor",
    instructions="contesta a las respuestas claro y conciso.",
    model="gpt-6-astra",
)

def load_configuration() -> None:
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    if not os.getenv("OPENAI_API_KEY", "").strip():
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configurala en .env o en las variables del entorno."
        )

async def main() -> None:
    result = await Runner.run(agent, "Cuando cayo el imperio Egipcio?")
    print(result.final_output)


if __name__ == "__main__":
    load_configuration()
    asyncio.run(main())
