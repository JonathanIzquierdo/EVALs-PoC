import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

JUDGE_PROMPT = """You are an expert evaluator for customer support AI responses.

Evaluate the AI response based on these criteria (score 1-5 for each):

1. EMPATHY: Does the response show understanding and care for the customer's situation?
   - 1: Cold, dismissive
   - 3: Neutral, professional
   - 5: Warm, genuinely understanding

2. CLARITY: Is the response clear, well-structured, and easy to understand?
   - 1: Confusing, unclear
   - 3: Understandable but could be clearer
   - 5: Crystal clear, well-organized

3. CORRECTNESS: Is the response appropriate and helpful for the customer's issue?
   - 1: Inappropriate or unhelpful
   - 3: Somewhat helpful
   - 5: Directly addresses the issue effectively

4. TONE: Is the tone professional and appropriate for customer support?
   - 1: Unprofessional or inappropriate
   - 3: Professional but generic
   - 5: Professional, friendly, and engaging

USER INPUT: {user_input}
AI RESPONSE: {ai_output}

Return ONLY a JSON object with the scores. Format:
{{"empathy": X.X, "clarity": X.X, "correctness": X.X, "tone": X.X}}
"""


def run_llm_judge(user_input: str, ai_output: str) -> dict:
    """
    Evaluate AI response using LLM as a judge
    
    Args:
        user_input: Original user message
        ai_output: AI-generated response
        
    Returns:
        Dictionary with evaluation scores
    """
    try:
        prompt = JUDGE_PROMPT.format(
            user_input=user_input,
            ai_output=ai_output
        )
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_DEPLOYMENT_ID", "gpt-4.1"),
            messages=[
                {"role": "system", "content": "You are an expert evaluator. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        
        # Parse JSON response
        scores = json.loads(result)
        
        # Validate all required keys are present
        required_keys = ["empathy", "clarity", "correctness", "tone"]
        for key in required_keys:
            if key not in scores:
                scores[key] = 3.0  # Default to neutral if missing
                
        return scores
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        # Return neutral scores if parsing fails
        return {
            "empathy": 3.0,
            "clarity": 3.0,
            "correctness": 3.0,
            "tone": 3.0
        }
    except Exception as e:
        raise Exception(f"Error running LLM judge: {str(e)}")


def passed_threshold(scores: dict) -> bool:
    """
    Check if LLM judge scores meet minimum thresholds
    
    Args:
        scores: Dictionary with evaluation scores
        
    Returns:
        True if all thresholds are met
    """
    thresholds = {
        "empathy": 3.5,
        "clarity": 3.0
    }
    
    for criterion, threshold in thresholds.items():
        if scores.get(criterion, 0) < threshold:
            return False
            
    return True
