# Semana 1 · ¿Quién ejecuta la herramienta?

El primer módulo del roadmap abarca dos semanas. En este primer ejercicio,
simulás la propuesta del modelo y observás cómo Python decide si la ejecuta.
Los pedidos son ficticios. No necesitás una API key.

Desde la raíz del repositorio, con el entorno virtual activo y las
dependencias del README instaladas:

1. Imaginá que alguien pregunta «¿Dónde está mi pedido PED-001?». En esta
   práctica vos escribís los argumentos que propondría el modelo:

   ```bash
   python -m labs.pedidos '{"id":"PED-001"}'
   ```

   El resultado esperado es `{"id": "PED-001", "estado": "en preparación"}`.
   El estado sale de los datos de Python. Probá también `PED-002` y `PED-999`:
   el segundo tiene formato válido, pero no existe en los datos.

2. Predecí qué ocurrirá con estas propuestas y después ejecutalas:

   ```bash
   python -m labs.pedidos '{"id":42}'
   python -m labs.pedidos '{"id":"PED-001"}' --sin-permiso
   python -m labs.pedidos '{"id":"PED-001"}' --herramienta cancelar_pedido
   ```

   Se rechazan por motivos distintos: argumentos inválidos, sesión sin permiso
   y herramienta fuera de la lista permitida. Ninguna llega a consultar datos.
   El permiso se simula fuera del JSON: es una decisión de la aplicación.

3. Verificá los casos con `python -m unittest discover -s tests -p test_pedidos.py`.

**Para cerrar la práctica:** explicá por qué «pedido inexistente» es un
resultado válido, mientras que «sin permiso» impide incluso buscarlo.
Después abrí `scripts/tools.py`: ubicá dónde llega el `function_call` y
dónde Python devuelve el resultado con el mismo `call_id`. Ese ejemplo
hace llamadas reales si lo ejecutás; para esta lectura no hace falta hacerlo.

El siguiente paso del módulo es reemplazar la propuesta manual por la del
modelo. El endpoint y la escritura con confirmación quedan para más adelante.

## Segunda práctica: preguntale al modelo

Desde la raíz, con el entorno virtual activo y `OPENAI_API_KEY` configurada:

```bash
python -m labs.pedidos_api "¿Ya salió mi pedido PED-002?"
```

Ahora escribís la pregunta. El modelo recibe la descripción de la herramienta
y su esquema generado desde Pydantic. Si propone una llamada, Python la pasa
a la misma función `ejecutar_propuesta` del primer ejercicio. El estado sale
del catálogo local. Una segunda petición devuelve ese resultado al modelo
con el mismo `call_id` para que lo explique en español.

Compará con «¿Ya salió mi pedido?» sin ID: la instrucción es pedir el dato
faltante. Si el modelo responde sin llamar a la herramienta, el programa
muestra ese texto y termina. Con `--sin-permiso` termina antes de contactar
con la API. El permiso de este CLI es simulado.

El ejercicio usa el SDK indicado en requirements.txt y hasta dos solicitudes
reales por ejecución, que pueden consumir saldo. El modelo predeterminado es
`gpt-6-astra`; podés configurar `OPENAI_MODEL` en el entorno o en .env.
Para practicar sin saldo, seguí usando el primer laboratorio o ejecutá
`python -m unittest discover -s tests -p test_pedidos_api.py` con respuestas
simuladas. Referencia: [Function calling de OpenAI](https://developers.openai.com/api/docs/guides/function-calling).
