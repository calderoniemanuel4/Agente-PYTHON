# AGENTS.md

## Propósito

Este archivo define las pautas de trabajo para los agentes que desarrollen este proyecto. El objetivo es construir una aplicación mantenible, segura y fácil de desplegar, usando Python y FastAPI, con integraciones externas, persistencia en Firestore y renderizado con Jinja2 cuando corresponda.

Las instrucciones de este archivo aplican a todo el repositorio. Si en el futuro se agrega un `AGENTS.md` dentro de un subdirectorio, sus instrucciones complementarán o reemplazarán estas reglas únicamente dentro de ese alcance.

## Principios generales

- Trabajar de forma metódica, incremental y verificable.
- Priorizar soluciones simples, claras y adecuadas al alcance real del proyecto.
- No sobreingenierizar la estructura, las abstracciones, los patrones ni la infraestructura.
- Evitar dependencias, capas, servicios, repositorios o configuraciones que no resuelvan una necesidad concreta.
- Mantener separadas las responsabilidades cuando esa separación mejore de forma tangible la legibilidad, las pruebas o el mantenimiento.
- Antes de modificar código existente, comprender su comportamiento, sus dependencias y sus pruebas.
- Preservar los cambios del usuario y evitar modificaciones ajenas a la tarea solicitada.
- No incluir secretos, tokens, credenciales ni datos sensibles en el código, los ejemplos, las pruebas, los logs o el repositorio.

## Stack y convenciones técnicas

### Python

- Usar una versión moderna y estable de Python compatible con las dependencias del proyecto.
- Seguir PEP 8 y aplicar type hints en funciones, métodos y estructuras relevantes.
- Preferir nombres descriptivos, funciones pequeñas y control de flujo explícito.
- Usar modelos de Pydantic para validar entradas, salidas, configuración y contratos cuando corresponda.
- Evitar estado global mutable y efectos secundarios ocultos.
- Capturar excepciones específicas; no ocultar errores con `except Exception` salvo en límites controlados donde se registren y traduzcan correctamente.
- Usar logging estructurado o consistente. Nunca registrar secretos ni información personal innecesaria.
- Administrar dependencias de forma explícita, reproducible y con versiones compatibles.
- Mantener configuración y secretos fuera del código mediante variables de entorno. Proveer un `.env.example` sin valores sensibles cuando sea útil.

### FastAPI y servicios web

- Usar FastAPI para APIs y servicios HTTP.
- Definir contratos claros: esquemas de entrada y salida, códigos de estado, errores y validaciones.
- Aprovechar la inyección de dependencias de FastAPI sin crear capas artificiales.
- Mantener los endpoints delgados cuando exista lógica de negocio reutilizable, pero no extraer abstracciones prematuramente.
- Documentar endpoints mediante nombres, descripciones, modelos y respuestas compatibles con OpenAPI.
- Implementar timeouts, manejo de errores, reintentos acotados e idempotencia cuando la integración lo requiera.
- Validar autenticidad, autorización y contenido de webhooks antes de procesarlos.
- Incluir endpoints de salud sólo cuando sean útiles para ejecución local, monitoreo o despliegue.

### Firestore

- Encapsular el acceso a Firestore únicamente al nivel necesario para evitar que detalles de persistencia contaminen la lógica de negocio.
- Definir de manera explícita colecciones, documentos, campos obligatorios y criterios de identificación.
- Evitar lecturas completas de colecciones y consultas innecesariamente costosas.
- Considerar índices, límites, paginación, concurrencia, transacciones y escrituras por lotes según el caso de uso.
- Usar timestamps consistentes y preferir timestamps generados por el servidor cuando corresponda.
- Diseñar las operaciones críticas para tolerar reintentos y evitar duplicados.
- Usar emuladores para pruebas locales siempre que resulte posible.

### Jinja2Templates

- Usar `Jinja2Templates` para vistas HTML renderizadas en el servidor cuando el proyecto las requiera.
- Mantener las plantillas enfocadas en presentación; la lógica de negocio debe resolverse antes del renderizado.
- Organizar templates, layouts, parciales y archivos estáticos de manera simple y coherente con el tamaño de la aplicación.
- Escapar contenido no confiable y no usar filtros que deshabiliten el escape sin una justificación concreta.
- No duplicar una arquitectura frontend compleja cuando Jinja2 y JavaScript puntual sean suficientes.

### Integraciones externas

- Siempre que se implemente una integración, un servicio web o una API, usar primero un MCP vigente y apropiado si está disponible.
- Si no existe un MCP vigente, consultar y utilizar la documentación oficial del proveedor o tecnología correspondiente antes de diseñar o implementar la solución.
- No basar una integración en recuerdos, ejemplos no oficiales, publicaciones antiguas o suposiciones cuando exista documentación oficial verificable.
- Registrar en el `README.md` o en la documentación técnica la fuente oficial utilizada, las versiones relevantes, los requisitos de configuración y las decisiones importantes.
- Confirmar autenticación, permisos, URLs, versiones de API, payloads, firmas, paginación, límites, webhooks, idempotencia y manejo de errores contra la documentación vigente.
- Aislar SDKs y clientes externos sólo lo necesario para facilitar pruebas y evitar que sus detalles se propaguen por toda la aplicación.
- No simular como exitosa una integración que no haya sido verificada; indicar con claridad cualquier limitación del entorno o credencial faltante.

### Cloud y despliegue

- Diseñar la aplicación para ejecutarse mediante configuración por entorno y sin depender del estado local del proceso.
- Mantener el despliegue reproducible y documentado.
- Aplicar el principio de mínimo privilegio a cuentas de servicio y permisos cloud.
- No desplegar hasta que la ejecución y las pruebas locales relevantes hayan sido completadas.
- Antes de un despliegue, revisar variables de entorno, secretos, región, proyecto/cuenta objetivo, costos previsibles, migraciones y compatibilidad.
- Después del despliegue, verificar salud, logs y al menos un flujo funcional crítico.

## Desarrollo por fases

Todo desarrollo significativo debe avanzar por las siguientes fases. Cada fase debe dejar un resultado verificable antes de continuar.

### 1. Planificación

- Comprender el objetivo, alcance, usuarios, flujos y criterios de aceptación.
- Identificar integraciones, datos, riesgos, requisitos de seguridad y restricciones del entorno.
- Consultar MCPs vigentes o documentación oficial según corresponda.
- Proponer una solución proporcional al problema y dividirla en entregables pequeños.
- Aclarar decisiones que cambien materialmente el alcance antes de implementarlas.

### 2. Scaffold

- Crear únicamente la estructura mínima necesaria para ejecutar y ampliar la aplicación.
- Evitar directorios vacíos, interfaces especulativas y capas reservadas para necesidades hipotéticas.
- Configurar dependencias, variables de entorno, punto de entrada y herramientas de calidad esenciales.
- Confirmar que la aplicación inicia localmente antes de sumar funcionalidad compleja.

### 3. README.md y documentación

- Crear o actualizar el `README.md` desde las primeras etapas; no dejarlo exclusivamente para el final.
- Incluir propósito, requisitos, instalación, configuración, variables de entorno, ejecución local, pruebas y despliegue.
- Documentar colecciones de Firestore, integraciones, webhooks y decisiones operativas relevantes.
- Mantener ejemplos ejecutables y libres de secretos.
- Actualizar la documentación junto con cualquier cambio de comportamiento o configuración.

### 4. Implementación y pruebas locales

- Implementar por flujos verticales pequeños y comprobables.
- Agregar pruebas proporcionales al riesgo: unitarias para lógica aislada e integración para límites HTTP, Firestore y proveedores externos cuando corresponda.
- Usar el emulador de Firestore y mocks/fakes controlados cuando no sea seguro o viable usar servicios reales.
- Probar las APIs localmente con Postman y mantener una colección reutilizable cuando aporte valor al proyecto.
- La colección de Postman debe usar variables de entorno y no contener tokens, credenciales ni datos sensibles.
- Verificar caminos exitosos, errores de validación, autenticación, fallos del proveedor, reintentos y duplicados relevantes.
- Ejecutar formatters, linters, chequeos de tipos y tests configurados antes de considerar terminada la fase.

### 5. Deploy y verificación

- Desplegar sólo con autorización y sobre el entorno explícitamente indicado.
- Usar un procedimiento repetible, preferentemente automatizado y documentado.
- Confirmar que secretos y configuración estén disponibles en el entorno de destino sin exponerlos.
- Ejecutar smoke tests posteriores al despliegue y revisar logs, estado y comportamiento del flujo crítico.
- Documentar el resultado, la URL o servicio desplegado, las verificaciones realizadas y cualquier seguimiento pendiente.

## Postman

- Usar Postman como herramienta principal para la validación manual y exploratoria de APIs cuando corresponda.
- Mantener colecciones y entornos exportables dentro del repositorio sólo si no contienen secretos.
- Incluir ejemplos de requests, respuestas esperadas, headers, autenticación y casos de error relevantes.
- Usar scripts de Postman únicamente cuando simplifiquen pruebas repetibles; evitar lógica compleja difícil de mantener.
- Las pruebas automatizadas del repositorio siguen siendo la fuente principal de regresión; Postman las complementa y no las reemplaza.

## Seguridad y datos

- Validar toda entrada en los límites del sistema.
- Aplicar autenticación y autorización explícitas a operaciones protegidas.
- Verificar firmas y prevenir replay attacks en webhooks cuando el proveedor lo soporte.
- No confiar en precios, permisos, identificadores sensibles ni estados enviados por el cliente sin validación del servidor.
- Reducir al mínimo la recopilación, exposición y persistencia de datos personales.
- No devolver trazas internas ni detalles sensibles en respuestas HTTP.
- Mantener secretos en el gestor de secretos del entorno o en variables seguras, nunca en Git.
- Informar cualquier riesgo de seguridad relevante descubierto durante el trabajo.

## Calidad y definición de terminado

Una tarea se considera terminada cuando, según su alcance:

- Cumple los criterios de aceptación.
- La implementación es simple y coherente con la arquitectura existente.
- Los contratos y errores de la API están definidos y verificados.
- Las pruebas locales relevantes pasan.
- La validación manual con Postman fue realizada o quedó documentada como pendiente por una limitación concreta.
- El `README.md` y la documentación afectada están actualizados.
- No se introdujeron secretos ni cambios ajenos a la tarea.
- Si hubo deploy, el servicio fue verificado en el entorno destino y el resultado quedó informado.

## Comunicación y toma de decisiones

- Informar supuestos, riesgos y bloqueos de forma concreta.
- No afirmar que una prueba, integración o despliegue funcionó si no se ejecutó y verificó.
- Ante documentación contradictoria, priorizar la fuente oficial vigente y dejar constancia de la decisión.
- Si una decisión implica costos, cambios irreversibles, permisos nuevos o expansión material del alcance, solicitar confirmación antes de proceder.
- Al entregar trabajo, resumir los cambios, las pruebas realizadas, el estado del deploy y los pendientes reales.
