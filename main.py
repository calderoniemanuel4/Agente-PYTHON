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

###  AQUI COMIENZA EL CODIGO PARA PROBAR ###

history_tutor = Agent(
    name="History tutor",
    handoff_description="Specialist for history questions.",
    instructions="Answer history questions clearly and concisely.",
)

math_tutor = Agent(
    name="Math tutor",
    handoff_description="Specialist for math questions.",
    instructions="Explain math step by step and include worked examples.",
)

triage_agent = Agent(
    name="Homework triage",
    instructions="Route each homework question to the right specialist.",
    handoffs=[history_tutor, math_tutor],
)


async def main() -> None:
    load_configuration()
    result = await Runner.run(
        triage_agent,
        "What is a circunference ?",
    )
    print(result.final_output)
    print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())
