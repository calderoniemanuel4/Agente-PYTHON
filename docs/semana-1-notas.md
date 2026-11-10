# Semana 1 · Notas, observaciones e informe de avance

Registro de las consultas surgidas durante la lectura del laboratorio.
Complementa la [guía práctica de la semana 1](semana-1.md), donde están los
ejercicios y comandos para ejecutar. Este archivo reúne explicaciones de
Python, validación y uso de herramientas con la API, organizadas por tema.

## Registro al 10 de noviembre de 2026

Se revisaron los conceptos siguientes a partir de `labs/pedidos.py` y
`labs/pedidos_api.py`. Este registro documenta lo conversado; no acredita
la ejecución de las prácticas ni una validación real de la API.

### 1. Argumentos de consola: guiones y guiones bajos

**Consulta:** si la opción es `--sin-permiso`, ¿por qué se escribe
`args.sin_permiso`?

`argparse` convierte los guiones de la opción en guiones bajos para el nombre
del atributo de Python:

```python
parser.add_argument("--sin-permiso", action="store_true")
# En consola: --sin-permiso
# En Python: args.sin_permiso
```

`args.sin-permiso` se interpretaría como una resta: `args.sin - permiso`.
Con `action="store_true"`, pasar la opción produce `True`; omitirla produce
`False`. Por eso `permite_lectura=not args.sin_permiso` permite leer cuando
la opción está ausente y lo impide cuando está presente.

### 2. Pydantic: configuración del modelo y restricciones del campo

**Consulta:** ¿`ConfigDict` y `Field` se superponen al hacer estricta la validación?

```python
class ConsultaPedido(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    id: str = Field(pattern=r"^PED-[0-9]{3}$")
```

Se complementan: `ConfigDict` configura el modelo y `Field` restringe un campo
concreto. La anotación `id: str` establece el tipo esperado.

| Regla | Qué controla | Ejemplo rechazado |
| --- | --- | --- |
| `extra="forbid"` | No admite campos adicionales | `{"id": "PED-123", "nombre": "Ana"}` |
| `strict=True` | Exige tipos compatibles sin conversiones automáticas permisivas | `{"id": 123}` |
| `Field(pattern=...)` | Exige `PED-` seguido de exactamente tres dígitos | `{"id": "ABC-123"}` |

`{"id": "PED-123"}` cumple esas reglas. Si los datos incumplen la validación,
Pydantic lanza `ValidationError` y no devuelve una instancia válida del modelo.
En el laboratorio, esto ocurre al ejecutar `ConsultaPedido.model_validate_json`.

Validar el formato no comprueba que el pedido exista: un identificador válido
puede devolver el estado `no encontrado` al consultar el catálogo.

### 3. JSON: `dumps` y `loads`

**Consulta:** ¿en qué sentido convierte cada función?

- `json.dumps(objeto)`: objeto Python → texto JSON (`str`).
- `json.loads(texto)`: texto JSON → objeto Python.

```python
texto = json.dumps({"id": "PED-123"})  # str: '{"id": "PED-123"}'
datos = json.loads(texto)              # dict: {"id": "PED-123"}
```

En el laboratorio, `json.dumps(resultado, ensure_ascii=False)` convierte el
resultado de la herramienta en texto JSON y conserva caracteres como las tildes.

### 4. Comprensiones de listas

**Consulta:** ¿cómo se llama esta forma abreviada de recorrer y filtrar?

```python
llamadas = [item for item in propuesta.output if item.type == "function_call"]
```

Es una **comprensión de listas** (*list comprehension*). En este caso equivale a:

```python
llamadas = []
for item in propuesta.output:
    if item.type == "function_call":
        llamadas.append(item)
```

La lista resultante contiene los elementos de tipo `function_call`, con sus
datos; no contiene solamente los nombres de las herramientas.

### 5. `with`: ciclo de vida del cliente

**Consulta:** ¿por qué usar `with` con OpenAI si también se usa con archivos
y para administrar recursos durante el ciclo de vida de una aplicación?

```python
with OpenAI(timeout=30, max_retries=0) as client:
    print(preguntar(client, ...))
```

`with` es una sentencia de Python que utiliza un **gestor de contexto**.
Aquí se crea el cliente, se utiliza dentro del bloque y se cierra al salir,
liberando sus conexiones HTTP incluso si ocurre una excepción.

La idea es la misma que con `with open(...)`: asegurar la limpieza del recurso.
En este CLI, el cliente dura lo que tarda la consulta. En una aplicación FastAPI,
puede administrarse desde el ciclo de vida para reutilizarlo mientras la
aplicación está en ejecución y cerrarlo al apagarla.

Este contexto administra recursos del programa. Las instrucciones y el historial
que recibe el modelo se envían por separado en las solicitudes.
Referencia consultada: [SDK oficial de OpenAI, gestión de recursos HTTP](https://developers.openai.com/api/reference/python#managing-http-resources).

### 6. El asterisco en la firma de una función

**Consulta:** ¿el `*` significa que `pregunta` puede recibir varios valores?

```python
def preguntar(client: OpenAI, pregunta: str, *, modelo: str, permite_lectura: bool) -> str:
    ...
```

El `*` solo exige pasar **por nombre** los parámetros que vienen después:

```python
preguntar(client, "¿Dónde está PED-001?", modelo="mi-modelo", permite_lectura=True)
```

Pasar el modelo y el permiso únicamente por posición genera `TypeError`.
`pregunta` sigue siendo un único `str`. La sintaxis `*args`, que reúne argumentos
posicionales en una tupla, tiene otra función.

### 7. Herramientas: solicitud del modelo y respuesta al usuario

**Consulta:** si la instrucción pide contestar en español, ¿por qué el modelo
devuelve una función en lugar de una respuesta redactada?

`propuesta.output` puede contener distintos tipos de elementos. Un elemento
`function_call` solicita ejecutar una herramienta e incluye su `name`, sus
`arguments` y un `call_id`. Los argumentos llegan como texto JSON.

El flujo del laboratorio es:

1. El modelo recibe la pregunta, las instrucciones y la definición de la herramienta.
2. Si necesita consultar un pedido, solicita `consultar_estado_pedido` con su ID.
3. Python valida la solicitud y ejecuta la lógica local mediante `ejecutar_propuesta`.
4. Python envía el resultado al modelo como `function_call_output`, asociado al mismo `call_id`.
5. El modelo redacta la respuesta en español usando ese resultado.

El nombre de la herramienta es un identificador técnico. La instrucción de
idioma orienta la respuesta dirigida al usuario. Si falta el ID, el modelo puede
pedirlo directamente en español sin solicitar una herramienta.

Aunque la API permite definir varias herramientas, este laboratorio define una
y rechaza que una respuesta proponga más de una llamada.

### 8. Cómo conoce el modelo una función de otro archivo

**Consulta:** ¿cómo detecta `consultar_estado_pedido` si no está definida ni
importada directamente en `pedidos_api.py`?

El modelo recibe la definición que la aplicación le envía:

```python
herramienta = {
    "type": "function",
    "name": "consultar_estado_pedido",
    # Descripción y esquema de parámetros definidos en el laboratorio.
}
# La solicitud incluye tools=[herramienta].
```

Conoce ese contrato; no inspecciona archivos Python ni descubre sus funciones.
Cuando devuelve una solicitud, el programa hace la conexión con la implementación:

```python
ejecutar_propuesta(llamada.name, llamada.arguments, permite_lectura=permite_lectura)
```

`ejecutar_propuesta` sí está importada desde `labs.pedidos`. En ese módulo,
valida el nombre permitido, comprueba el permiso, valida los argumentos con
Pydantic y llama a `consultar_estado_pedido`.

En este proyecto, el nombre de la herramienta coincide con el de la función
Python. Esa coincidencia es una decisión de implementación: el contrato enviado
al modelo podría usar otro nombre si el código lo asociara explícitamente.

## Observación sobre el ritmo del roadmap

Surgió la duda de si las consultas harán que el recorrido supere las diez semanas.
Se tomó ese plazo como una guía ajustable: comprender las piezas y resolver dudas
también forma parte del avance. No se fijó un nuevo plazo ni se modificó el alcance.

## Punto de pausa y continuidad

La sesión se cerró después de aclarar cómo el contrato de una herramienta se
conecta con la función local que la ejecuta. Al retomar, la referencia práctica
sigue siendo la [segunda práctica de la semana 1](semana-1.md#segunda-práctica-preguntale-al-modelo).

Las próximas observaciones pueden agregarse como registros fechados, manteniendo
las preguntas y sus explicaciones por tema. Los comandos y casos prácticos
continúan en la guía del laboratorio.
