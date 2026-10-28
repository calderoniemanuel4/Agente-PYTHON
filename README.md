# Agente-PYTHON
Un ejemplo de llamada a la Responses API de OpenAI desde Python.

## Ejecución local

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crear `.env` en la raíz del proyecto (un nivel arriba de `scripts/`) si no existe; si ya existe, conservarlo.
Editar `.env` y asignar una clave de OpenAI a `OPENAI_API_KEY`
(nombre exacto, en mayúsculas y con la `I` de `OPENAI`). Luego ejecutar:

```bash
python "scripts/uso de tokens.py"
```

Los scripts de `scripts/` cargan el mismo `.env` de la raíz mediante `python-dotenv`,
sin sobrescribir variables ya definidas en el entorno. Validan la clave y la
entregan al cliente `OpenAI`. `uso de tokens.py` e `image analizer.py` llaman a
`responses.create` y muestran después del texto los tokens de entrada, salida
y total que devuelve `response.usage`; si la API no informa el uso, lo indican
sin inventar cifras.
Si falta `OPENAI_API_KEY` o está vacía, termina antes de llamar a la API.
La ejecución requiere acceso al modelo configurado y puede consumir saldo de la API.

`python scripts/tools.py` demuestra function calling con `get_weather`: devuelve
una temperatura simulada de 18 °C, marcada como dato ficticio. Hace una segunda
llamada a la API para que el modelo redacte la respuesta; no consulta el clima real.

`.env` está excluido de Git.
Los secretos se guardan como texto local, por lo que no deben incluirse en logs ni commits.

Dependencias: `openai==3.37.0`, `openai-agents==0.24.0` y `python-dotenv==1.2.1`.
Referencia oficial: [python-dotenv](https://github.com/theskumar/python-dotenv/tree/v1.2.1).
Configuración de la clave: [OpenAI Developer Quickstart](https://developers.openai.com/api/docs/quickstart).
Uso de tokens: [referencia oficial de Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create).

## Pruebas locales

```bash
python -m unittest discover -s tests -v
```

Las pruebas usan valores ficticios y simulan `responses.create`: verifican que los
tres scripts carguen `.env` desde la raíz, la prioridad del entorno y el rechazo
de claves ausentes o vacías, sin llamadas a la API. La autenticación real con
OpenAI se verifica por separado al ejecutar uno de los scripts.
Postman no aplica: este proyecto se ejecuta por consola y no expone endpoints HTTP.
