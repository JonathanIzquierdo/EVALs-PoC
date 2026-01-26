from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_client import generate_answer
from evaluators.deterministic import run_deterministic_evals
from evaluators.llm_judge import run_llm_judge, passed_threshold
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Evals PoC - Customer Support Assistant")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    evaluations: dict
    final_status: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    AI customer support endpoint with real-time evaluation
    """
    try:
        # Generate AI answer
        logger.info(f"Processing message: {request.message[:50]}...")
        ai_answer = generate_answer(request.message)
        logger.info(f"Generated answer: {ai_answer[:50]}...")
        
        # Run deterministic evaluations
        deterministic_results = run_deterministic_evals(ai_answer)
        logger.info(f"Deterministic evals: {deterministic_results}")
        
        # Run LLM judge evaluation
        llm_judge_results = run_llm_judge(request.message, ai_answer)
        logger.info(f"LLM judge scores: {llm_judge_results}")
        
        # Check if LLM judge passed thresholds
        llm_passed = passed_threshold(llm_judge_results)
        
        # Determine final status
        all_deterministic_passed = all(deterministic_results.values())
        final_status = "PASS" if (all_deterministic_passed and llm_passed) else "FAIL"
        
        evaluations = {
            "deterministic": deterministic_results,
            "llm_judge": llm_judge_results,
            "llm_judge_passed": llm_passed
        }
        
        logger.info(f"Final status: {final_status}")
        
        return ChatResponse(
            answer=ai_answer,
            evaluations=evaluations,
            final_status=final_status
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
