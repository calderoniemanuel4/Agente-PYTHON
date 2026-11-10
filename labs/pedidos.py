"""Semana 1: ejecutar una propuesta de herramienta sin llamar a una API."""

import argparse
import json
import sys

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ConsultaPedido(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: str = Field(pattern=r"^PED-[0-9]{3}$")


def consultar_estado_pedido(id: str) -> dict[str, str]:
    pedidos = {"PED-001": "en preparación", "PED-002": "enviado"}
    return {"id": id, "estado": pedidos.get(id, "no encontrado")}


def ejecutar_propuesta(nombre: str, argumentos: str, *, permite_lectura: bool) -> dict[str, str]:
    if nombre != "consultar_estado_pedido":
        raise ValueError("Herramienta no permitida.")
    if not permite_lectura:
        raise PermissionError("No hay permiso para consultar pedidos.")
    consulta = ConsultaPedido.model_validate_json(argumentos)
    return consultar_estado_pedido(consulta.id)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("argumentos", help='JSON de la propuesta, por ejemplo: {"id":"PED-001"}')
    parser.add_argument("--herramienta", default="consultar_estado_pedido")
    parser.add_argument("--sin-permiso", action="store_true", help="Simula una sesión sin acceso.")
    args = parser.parse_args()
    try:
        resultado = ejecutar_propuesta(
            args.herramienta, args.argumentos, permite_lectura=not args.sin_permiso
        )
    except ValidationError:
        parser.exit(1, "Argumentos inválidos: se espera solo id con formato PED-001.\n")
    except (PermissionError, ValueError) as error:
        sys.exit(str(error))
    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == "__main__":
    main()
