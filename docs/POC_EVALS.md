# Documentación de la PoC de Evals

Esta documentación explica cómo funciona la Prueba de Concepto (PoC) del producto demo de Evals, que incluye un evaluador determinista y un juez de LLM. A continuación se detallan los componentes y el flujo de trabajo involucrados en la PoC.

## Productos Demonstração

La PoC incluye un producto de demostración que simula el funcionamiento del sistema de evaluación utilizando técnicas avanzadas de inteligencia artificial.

## Evaluador Determinista

El evaluador determinista es responsable de realizar evaluaciones basadas en criterios predefinidos. Su funcionamiento asegura que las evaluaciones sean repetibles y consistentes.

## Juez LLM

El juez de LLM (Modelo de Lenguaje de Gran Escala) evalúa respuestas generadas por el sistema en comparación con las expectativas definidas, utilizando texto natural y técnicas de NLP.

## Pipeline de Run AI Evals

El pipeline "run_ai_evals" integra todos los componentes de la evaluación automatizada, desde la entrada de datos hasta la generación de resultados.

## Flujo de Trabajo de GitHub Actions

La automatización de CI/CD se maneja a través de un flujo de trabajo de GitHub Actions, que asegura que las pruebas y evaluaciones se desarrollen de manera continua. Se puede encontrar el archivo de configuración aquí: [GitHub Actions Workflow](https://github.com/JonathanIzquierdo/EVALs-PoC/blob/main/.github/workflows/your_workflow.yml)

## Archivos Relevantes

- [Evaluador Determinista](https://github.com/JonathanIzquierdo/EVALs-PoC/blob/main/evaluator_deterministic.py)
- [Juez LLM](https://github.com/JonathanIzquierdo/EVALs-PoC/blob/main/llm_judge.py)
- [Pipeline de Run AI Evals](https://github.com/JonathanIzquierdo/EVALs-PoC/blob/main/run_ai_evals.py)

La documentación será actualizada según sea necesario para reflejar cambios en la PoC y su funcionalidad.