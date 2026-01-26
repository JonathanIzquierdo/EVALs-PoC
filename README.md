<<<<<<< HEAD
# AI Evals PoC

A Proof of Concept for evaluating AI customer support responses using both deterministic rules and LLM-based judging in a CI/CD pipeline.

## Overview

This project demonstrates a production-ready approach to AI quality assurance by implementing:

- **AI Customer Support Assistant**: A FastAPI service that generates responses to customer inquiries
- **Deterministic Evaluators**: Rule-based checks for policy compliance (apologies, escalation, PII protection, length)
- **LLM Judge**: AI-powered evaluation of response quality (empathy, clarity, correctness, tone)
- **CI Pipeline Integration**: Automated testing that fails builds when quality standards aren't met

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User      │────▶│  FastAPI /chat   │────▶│  LLM Client     │
│   Request   │     │   Endpoint       │     │  (OpenAI)       │
└─────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Evaluators     │
                    ├──────────────────┤
                    │ • Deterministic  │
                    │ • LLM Judge      │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Pass/Fail       │
                    │  Response        │
                    └──────────────────┘
```

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Setup

1. Clone the repository and navigate to the project folder:

```bash
cd EVALsPoC
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

## Running Locally

### Start the API Server

```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Me cobraron dos veces este mes"}'
```

Expected response:

```json
{
  "answer": "Lo siento mucho por este inconveniente...",
  "evaluations": {
    "deterministic": {
      "apology_present": true,
      "escalation_offer": true,
      "no_pii": true,
      "max_length": true
    },
    "llm_judge": {
      "empathy": 4.5,
      "clarity": 4.0,
      "correctness": 4.2,
      "tone": 4.3
    },
    "llm_judge_passed": true
  },
  "final_status": "PASS"
}
```

### Run AI Evals Pipeline

Execute the evaluation script that the CI pipeline uses:

```bash
python run_ai_evals.py
```

This will:
1. Load test cases from `test_cases.json`
2. Generate AI responses for each case
3. Run all evaluators
4. Print a detailed report
5. Exit with code 0 (success) or 1 (failure)

## How AI Evals Work

### Deterministic Evaluators

Located in `evaluators/deterministic.py`, these checks enforce hard rules:

- **Apology Present**: Ensures empathetic language (e.g., "lo siento", "lamento")
- **Escalation Offer**: Verifies human support is offered when appropriate
- **No PII**: Prevents requesting/exposing sensitive data (SSN, credit cards, passwords)
- **Max Length**: Enforces response brevity (≤200 words)

### LLM Judge

Located in `evaluators/llm_judge.py`, uses GPT to score responses on:

- **Empathy** (1-5): Understanding and care for customer's situation
- **Clarity** (1-5): Clear, well-structured communication
- **Correctness** (1-5): Appropriate and helpful response
- **Tone** (1-5): Professional and engaging

**Thresholds**:
- Empathy ≥ 3.5
- Clarity ≥ 3.0

### Test Cases

Edit `test_cases.json` to add more scenarios:

```json
[
  {"input": "Me cobraron dos veces este mes"},
  {"input": "Quiero cancelar mi cuenta"},
  {"input": "No funciona mi tarjeta"},
  {"input": "Your custom test case"}
]
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ai_evals.yml`) automatically runs on every push and pull request:

1. Sets up Python environment
2. Installs dependencies
3. Runs `run_ai_evals.py`
4. **Fails the build** if any test case doesn't meet quality standards

This ensures AI responses maintain consistent quality standards before deployment.

### Setting Up GitHub Actions

1. Add your OpenAI API key as a GitHub secret:
   - Go to repository Settings → Secrets → Actions
   - Add `OPENAI_API_KEY` with your API key

2. Push to trigger the workflow:

```bash
git push origin main
```

## Project Structure

```
EVALsPoC/
├── app.py                    # FastAPI application
├── llm_client.py             # OpenAI integration
├── run_ai_evals.py           # CI pipeline script
├── test_cases.json           # Evaluation test cases
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment template
├── evaluators/
│   ├── __init__.py
│   ├── deterministic.py      # Rule-based evaluators
│   └── llm_judge.py          # LLM-based evaluators
└── .github/
    └── workflows/
        └── ai_evals.yml      # GitHub Actions pipeline
```

## Adding New Evaluators

### Deterministic Evaluator

Add a new function to `evaluators/deterministic.py`:

```python
def check_custom_rule(text: str) -> bool:
    # Your logic here
    return result

# Update run_deterministic_evals to include it
def run_deterministic_evals(text: str) -> dict:
    return {
        # ... existing checks
        "custom_rule": check_custom_rule(text)
    }
```

### LLM Judge Criteria

Modify the `JUDGE_PROMPT` in `evaluators/llm_judge.py` to add new scoring dimensions.

## Troubleshooting

### API Key Issues

```
Error: OpenAI API key not found
```

**Solution**: Verify `.env` file exists and contains valid `OPENAI_API_KEY`

### Import Errors

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Ensure virtual environment is activated and dependencies are installed

### Test Failures

Review the evaluation report to identify which checks failed and adjust either:
- The AI prompt (in `llm_client.py`)
- The evaluation thresholds (in `evaluators/llm_judge.py`)
- The test cases (in `test_cases.json`)

## Best Practices

1. **Version Control Evals**: Track changes to evaluators and thresholds
2. **Monitor False Positives**: Regularly review failed cases for accuracy
3. **Iterate on Prompts**: Improve AI responses based on eval insights
4. **Expand Test Coverage**: Add diverse, real-world test cases
5. **Document Changes**: Update README when modifying evaluation criteria

## License

This is a Proof of Concept for demonstration purposes.

## Contact

For questions or improvements, please open an issue in the repository.
=======
# EVALs-PoC
EVALs - Pipelines
>>>>>>> 6504d74b0afb1a00d2282471082a8a7a6f475bbe
