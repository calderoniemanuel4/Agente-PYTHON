"""Semana 1: preguntar por un pedido en lenguaje natural."""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI
from pydantic import ValidationError

from labs.pedidos import ConsultaPedido, ejecutar_propuesta


def preguntar(client: OpenAI, pregunta: str, *, modelo: str, permite_lectura: bool) -> str:
    if not permite_lectura:
        raise PermissionError("No hay permiso para consultar pedidos.")

    herramienta = {
        "type": "function",
        "name": "consultar_estado_pedido",
        "description": "Consulta el estado de un pedido ficticio por su identificador.",
        "parameters": ConsultaPedido.model_json_schema(),
        "strict": True,
    }
    propuesta = client.responses.create(
        model=modelo,
        instructions=(
            "Contestá en español. Si hay un ID de pedido, usá la herramienta para "
            "consultarlo. Si falta, pedilo. No inventes identificadores ni estados."
        ),
        input=pregunta,
        tools=[herramienta],
        parallel_tool_calls=False,
    )
    llamadas = [item for item in propuesta.output if item.type == "function_call"]
    if not llamadas:
        return propuesta.output_text or "No se recibió una respuesta del modelo."
    if len(llamadas) != 1:
        raise ValueError("El laboratorio admite una consulta por turno.")
    llamada = llamadas[0]
    resultado = ejecutar_propuesta(llamada.name, llamada.arguments, permite_lectura=permite_lectura)
    final = client.responses.create(
        model=modelo,
        previous_response_id=propuesta.id,
        instructions="Respondé en español usando el resultado de la consulta ficticia.",
        input=[{
            "type": "function_call_output",
            "call_id": llamada.call_id,
            "output": json.dumps(resultado, ensure_ascii=False),
        }],
        tools=[herramienta],
        tool_choice="none",
    )
    return final.output_text or "No se recibió una respuesta final del modelo."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pregunta")
    parser.add_argument("--sin-permiso", action="store_true")
    args = parser.parse_args()
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    if args.sin_permiso:
        sys.exit("No hay permiso para consultar pedidos.")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        sys.exit("Falta OPENAI_API_KEY en .env o en el entorno.")
    try:
        with OpenAI(timeout=30, max_retries=0) as client:
            print(preguntar(client, args.pregunta, modelo=os.getenv("OPENAI_MODEL") or "gpt-6-astra",
                            permite_lectura=not args.sin_permiso))
    except ValidationError:
        sys.exit("El modelo propuso argumentos inválidos para consultar el pedido.")
    except (ValueError, PermissionError) as error:
        sys.exit(str(error))
    except APIStatusError as error:
        sys.exit(f"La API rechazó la solicitud (HTTP {error.status_code}).")
    except APIConnectionError:
        sys.exit("No se pudo conectar con la API dentro del tiempo disponible.")


if __name__ == "__main__":
    main()
