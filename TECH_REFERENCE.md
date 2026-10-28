# TECH_REFERENCE.md

> Apuntes de trabajo sobre la documentación oficial de OpenAI para este proyecto Python.
>
> Actualizado: 2026-10-27

---

## 1. Quickstart: API key y variables de entorno

**Fuente oficial:** [OpenAI Developer Quickstart](https://developers.openai.com/api/docs/quickstart), sección «Create and export an API key».

### Obtener la clave

1. Entrar al [panel de claves de la API de OpenAI](https://platform.openai.com/api-keys) y crear una API key.
2. Guardarla en un lugar seguro. No copiarla en el código, los apuntes, los logs ni un commit.

### Guardarla en `.env`

Crear un archivo `.env` en la raíz del proyecto, un nivel arriba de `scripts/`, con esta estructura:

```dotenv
OPENAI_API_KEY=tu_clave_aqui
```

El nombre de la variable es exactamente `OPENAI_API_KEY`. El archivo `.env` está excluido de Git mediante `.gitignore`. El ejemplo de arriba es solo un marcador: nunca escribir una clave real en este documento.

### Cargarla en el entorno del programa

Un archivo `.env` por sí solo no crea una variable de entorno. En este proyecto, `python-dotenv` lo carga desde la raíz al iniciar cualquiera de los scripts:

```python
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
api_key = os.getenv("OPENAI_API_KEY", "").strip()
```

`override=False` conserva el valor de `OPENAI_API_KEY` si ya está definido en el entorno del proceso. Los scripts validan que la clave no esté vacía y la entregan al cliente `OpenAI`. Los ejemplos de uso de tokens e imágenes llaman luego a `responses.create`. Ver [scripts/](scripts/).

La guía oficial muestra otra forma para la terminal de macOS/Linux:

```bash
export OPENAI_API_KEY="tu_clave_aqui"
```

Ese `export` vale para la sesión actual de la terminal. Los SDK de OpenAI pueden leer `OPENAI_API_KEY` desde el entorno. Para el flujo local de este proyecto, usar `.env` evita tener que repetir el `export` en cada terminal.

**Comprobación sin mostrar el secreto:** ejecutar `python "scripts/uso de tokens.py"`. Si la variable falta o está vacía, el programa termina con el mensaje «Falta OPENAI_API_KEY». Si está configurada, continúa hacia la llamada al modelo, que requiere acceso a la API y puede generar consumo.

---

## 2. Conteo de tokens por respuesta

**Fuentes oficiales:** [referencia de Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create) y [guía para contar tokens](https://developers.openai.com/api/docs/guides/token-counting).

Después de cada llamada a `client.responses.create(...)`, la respuesta puede incluir `usage`:

```python
response = client.responses.create(model="gpt-6-astra", input="Hola")
print(response.output_text)

if response.usage is not None:
    print(f"Entrada: {response.usage.input_tokens}")
    print(f"Salida: {response.usage.output_tokens}")
    print(f"Total: {response.usage.total_tokens}")
else:
    print("Uso de tokens no disponible")
```

- `input_tokens`: tokens procesados como entrada, que pueden incluir más que el texto del usuario.
- `output_tokens`: tokens generados por el modelo. Pueden superar los del texto visible porque también cuentan contenido no visible, como tokens de razonamiento o estructura.
- `total_tokens`: suma de entrada y salida para esa respuesta.

Los detalles opcionales están en `input_tokens_details` (por ejemplo, tokens en caché) y `output_tokens_details` (por ejemplo, tokens de razonamiento). Son desgloses de las cifras anteriores: no se suman otra vez al total. Si `usage` es `None`, no conviene mostrar cero como si fuera una medición real.

En este proyecto, [uso de tokens.py](scripts/uso%20de%20tokens.py) imprime las tres cifras después de la respuesta. Es una medición **por llamada a la API**; ese script hace una llamada por ejecución.

---

## 3. El parámetro `input` en el ejemplo de imagen

**Fuente oficial:** [OpenAI Developer Quickstart](https://developers.openai.com/api/docs/quickstart), ejemplo de entrada con imagen en Python.

En [image analizer.py](scripts/image%20analizer.py), `input` es la información que se envía al modelo. Es una lista con un mensaje del usuario (`role: "user"`). Dentro de `content`, ese mensaje combina dos partes:

```python
input=[
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": "What teams are playing in this image?"},
            {"type": "input_image", "image_url": "https://.../imagen.jpg"},
        ],
    }
]
```

`input_text` contiene la pregunta y `input_image` señala la imagen mediante una URL. Al estar en el mismo mensaje, el modelo recibe ambos elementos para responder a la pregunta sobre esa imagen. Para una consulta solo de texto, `input` también puede ser una cadena simple, como en [uso de tokens.py](scripts/uso%20de%20tokens.py).

---

## 4. Tools y function calling

**Fuente oficial:** [OpenAI Developer: Function calling](https://developers.openai.com/api/docs/guides/function-calling).

En [tools.py](scripts/tools.py), `tools` **describe** la función `get_weather` para el modelo: su nombre, qué hace y el argumento obligatorio `location`. El esquema exige que `location` sea texto y, con `strict: True`, limita los argumentos a los campos declarados.

La consulta pregunta por el clima de París. Si el modelo decide usar la herramienta, la primera respuesta puede contener un elemento `function_call` con datos como estos (ejemplo ilustrativo; el valor exacto de `location` lo elige el modelo):

```json
{
  "type": "function_call",
  "name": "get_weather",
  "arguments": "{\"location\":\"Paris, France\"}",
  "call_id": "call_..."
}
```

**¿Qué devuelve en este caso?** La primera respuesta puede incluir una **solicitud de llamada** a `get_weather`, con el argumento `location` y un `call_id`. Esa solicitud todavía no contiene una temperatura. El script actual lee la llamada, ejecuta `get_weather` y envía el resultado como `function_call_output` en una segunda solicitud; después imprime la respuesta final del modelo.

Para completar el flujo, hay que **definir también la función en Python**. El script actual usa esta versión de demostración:

```python
def get_weather(location: str) -> dict[str, str | int | bool]:
    return {"location": location, "temperature": 18, "unit": "C", "simulated": True}
```

El valor `18` es inventado: una versión real tendría que consultar un proveedor meteorológico. La marca `simulated: True` y el prompt del ejemplo indican al modelo que no presente esa cifra como clima actual. El programa usa el mismo `call_id` para asociar el resultado con la llamada original.

El script fuerza el uso de `get_weather` con `tool_choice={"type": "function", "name": "get_weather"}`. Aun así, recorre `response.output` y revisa el `type` de cada elemento, porque la respuesta puede contener otros tipos de elementos además de la llamada.

---

## Próximos apuntes

Agregar nuevas secciones a medida que avance el Quickstart y anotar en cada una la fuente oficial consultada.
