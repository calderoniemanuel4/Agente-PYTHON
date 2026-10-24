# Agente-PYTHON
Una App que utiliza un LLM para ejecutar funciones y tools

## Ejecución local

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crear `.env` junto a `main.py` si no existe; si ya existe, conservarlo.
Editar `.env` y asignar una clave de OpenAI a `OPENAI_API_KEY`
(nombre exacto, en mayúsculas y con la `I` de `OPENAI`). Luego ejecutar:

```bash
python main.py
```

El script carga el `.env` ubicado junto a `main.py` mediante `python-dotenv`,
sin sobrescribir variables ya definidas en el entorno. Al iniciar `main()`, valida
la clave y la registra en el SDK con `set_default_openai_key` antes de ejecutar
`Runner.run`. Si falta `OPENAI_API_KEY`
o está vacía, termina con un mensaje antes de llamar a la API.
La ejecución requiere acceso al modelo configurado y puede consumir saldo de la API.

`.env` está excluido de Git.
Los secretos se guardan como texto local, por lo que no deben incluirse en logs ni commits.

Dependencias directas: `openai-agents==0.24.0` y `python-dotenv==1.2.1`.
Referencia oficial: [python-dotenv](https://github.com/theskumar/python-dotenv/tree/v1.2.1).
Configuración del SDK: [OpenAI Agents SDK: API key](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory#prerequisites).

## Pruebas locales

```bash
python -m unittest discover -s tests -v
```

Las pruebas usan valores ficticios y simulan `Runner.run`: verifican la carga de
`.env`, la prioridad del entorno y el rechazo de claves ausentes o vacías antes
de ejecutar el agente, sin llamadas ni consumo de la API. La autenticación real
con OpenAI se verifica por separado al ejecutar `python main.py`.
Postman no aplica: este proyecto se ejecuta por consola y no expone endpoints HTTP.
