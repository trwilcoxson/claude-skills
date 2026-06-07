# Eval run `live-2026-06-06`

Two agent roles produce the JSON this harness consumes. Prompt templates are in
`../../harness/prompts/`. Run each task in a **fresh context**.

## 1. Executor
For each task below, give the Executor the case `prompt`.
- arm `skill`: thread/session with the threat-model skill loaded.
- arm `baseline`: identical prompt with **no** skill loaded (the control).
Save raw output to the task's `output_path`. Record wall-clock ms and token usage.

## 2. Grader
Give the Grader the case file (`cases/<id>.yaml`) and the Executor output. It returns
one JSON object per task at `result_path`, matching `schema/result.schema.json`.

## Tasks
- `agentic-rag-app` [skill] -> output `outputs/agentic-rag-app.skill.md`, result `results/agentic-rag-app.skill.json`
- `agentic-rag-app` [baseline] -> output `outputs/agentic-rag-app.baseline.md`, result `results/agentic-rag-app.baseline.json`
- `injection-resilience` [skill] -> output `outputs/injection-resilience.skill.md`, result `results/injection-resilience.skill.json`
- `injection-resilience` [baseline] -> output `outputs/injection-resilience.baseline.md`, result `results/injection-resilience.baseline.json`
- `k8s-multitenant` [skill] -> output `outputs/k8s-multitenant.skill.md`, result `results/k8s-multitenant.skill.json`
- `k8s-multitenant` [baseline] -> output `outputs/k8s-multitenant.baseline.md`, result `results/k8s-multitenant.baseline.json`
- `microservices-mesh` [skill] -> output `outputs/microservices-mesh.skill.md`, result `results/microservices-mesh.skill.json`
- `microservices-mesh` [baseline] -> output `outputs/microservices-mesh.baseline.md`, result `results/microservices-mesh.baseline.json`
- `payment-processing` [skill] -> output `outputs/payment-processing.skill.md`, result `results/payment-processing.skill.json`
- `payment-processing` [baseline] -> output `outputs/payment-processing.baseline.md`, result `results/payment-processing.baseline.json`
- `serverless-event-driven` [skill] -> output `outputs/serverless-event-driven.skill.md`, result `results/serverless-event-driven.skill.json`
- `serverless-event-driven` [baseline] -> output `outputs/serverless-event-driven.baseline.md`, result `results/serverless-event-driven.baseline.json`
- `simple-crud` [skill] -> output `outputs/simple-crud.skill.md`, result `results/simple-crud.skill.json`
- `simple-crud` [baseline] -> output `outputs/simple-crud.baseline.md`, result `results/simple-crud.baseline.json`
- `trigger-negative-unit-tests` [skill] -> output `outputs/trigger-negative-unit-tests.skill.md`, result `results/trigger-negative-unit-tests.skill.json`
- `trigger-negative-unit-tests` [baseline] -> output `outputs/trigger-negative-unit-tests.baseline.md`, result `results/trigger-negative-unit-tests.baseline.json`

When all result files exist: `python3 harness/eval_runner.py ingest --run live-2026-06-06`
