# Documentación Técnica sobre Evaluaciones de AI

## Evaluaciones Concretas Realizadas
### Evaluaciones Deterministas y Juez LLM
Se realizaron evaluaciones deterministas que incluyen descripciones de pruebas y evaluaciones por un Juez basado en LLM.

## Casos de Prueba y Suites
### Casos de Test desde test_cases.json
Para cada evaluación se definirán los siguientes elementos:
- **Entrada:** Datos de entrada para la evaluación
- **Salida Esperada:** Resultados que se anticipan
- **Criterio de Evaluación:** Parámetros según los cuales se evalúan los resultados
- **Umbral:** Valor mínimo aceptable para considerar el evaluador como exitoso
- **Evidencia:** Documentación o logs que respaldan la evaluación

## Detalles de la Implementación del Evaluador Determinista
- **Métodos Utilizados:** Regex, conteo de palabras, heurísticas lingüísticas.
- **Puntuación:** `0` o `1` dependiendo de la evaluación.
- **Normalización:** Proceso usado para ajustar los resultados.
- **Casos Límite:** Ejemplos y tratamientos para entradas excepcionales.

## Detalles de la Implementación del LLM como Juez
- **Modelo Utilizado:** AzureOpenAI con el ID de despliegue por defecto para gpt-4.1.
- **Configuraciones de API:**
  - `OPENAI_DEPLOYMENT_ID`
  - `OPENAI_API_VERSION`
  - `OPENAI_ENDPOINT`
- **Parámetros:**
  - Temperatura: `0.3`
  - Máx. tokens: `200`
  - Estructura del prompt: `JUDGE_PROMPT`
- **Validación de JSON y Parsado:** Estrategias para asegurar que la respuesta del modelo sea correcta.
- **Umbrales:**
  - Empatía: `>=3.5`
  - Claridad: `>=3.0`

## Formato del Conjunto de Datos y Resultados
- **Casos de Prueba:** Formato JSON en `test_cases.json`.
- **Reporte:** Impresión en consola con los resultados.
- **Artefactos:** Archivos con extensión `*.log` y `test_cases.json` subidos por el flujo de trabajo.

## Fases del Pipeline run_ai_evals y Ejemplos de CLI
- Revisar el archivo `.env.example` para variables de entorno necesarias.

## Comportamiento del Workflow de GitHub Actions
Revisar `.github/workflows/ai_evals.yml` para:
- **Disparadores:** Eventos que inician el flujo de trabajo.
- **Modo API:** Configuración del modo de operación.
- **Iniciación del Servidor:** Cómo se inicia la evaluación.
- **Salud del Servidor:** Verificaciones de salud de las evaluaciones (health check).
- **Condiciones de Fallo:** Definición de escenarios que causan fallos en el flujo de trabajo.
- **Artefactos Generados:** Archivos producidos durante la ejecución del workflow.