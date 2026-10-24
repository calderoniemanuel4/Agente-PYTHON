import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

def load_configuration() -> None:
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "Falta OPENAI_API_KEY. Configurala en .env o en las variables del entorno."
        )
    set_default_openai_key(api_key)


###  AQUI COMIENZA EL CODIGO PARA PROBAR ###


from agents import Agent, Runner, function_tool, set_default_openai_key

@function_tool
def history_fun_fact() -> str:
    """Return a short history fact."""
    return "Sharks are older than trees."


agent = Agent(
    name="History tutor",
    instructions="Answer history questions clearly. Use history_fun_fact when it helps.",
    tools=[history_fun_fact],
)


async def main() -> None:
    load_configuration()
    result = await Runner.run(
        agent,
        "Tell me something surprising about ancient life on Earth.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
