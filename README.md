# Agente-PYTHON
Una App que utiliza un LLM para ejecutar funciones y tools

## Ejecución local

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Si ya existe `.env`, conservarlo y completar las variables faltantes.
Editar `.env` y asignar una clave de OpenAI a `OPENAI_API_KEY`. Luego ejecutar:

```bash
python main.py
```

El script carga el `.env` ubicado junto a `main.py` mediante `python-dotenv`,
sin sobrescribir variables ya definidas en el entorno. Si falta `OPENAI_API_KEY`
o está vacía, termina con un mensaje antes de llamar a la API.
La ejecución requiere acceso al modelo configurado y puede consumir saldo de la API.

`.env` está excluido de Git; `.env.example` contiene únicamente nombres de variables.
Los secretos se guardan como texto local, por lo que no deben incluirse en logs ni commits.

Dependencias directas: `openai-agents==0.24.0` y `python-dotenv==1.2.1`.
Referencia oficial: [python-dotenv](https://github.com/theskumar/python-dotenv/tree/v1.2.1).
