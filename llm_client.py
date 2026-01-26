import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

SYSTEM_PROMPT = """You are a customer support assistant for a SaaS company.

Guidelines:
- Respond in the SAME LANGUAGE as the user's message
- Be empathetic and understanding when customers have issues
- Provide clear and helpful information
- Identify when to escalate to human support
- Keep responses concise and professional (under 200 words)
- Never share or ask for personal identifying information (PII)
"""


def generate_answer(user_message: str) -> str:
    """
    Generate AI response using OpenAI API
    
    Args:
        user_message: User's input message
        
    Returns:
        AI-generated response
    """
    try:
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_DEPLOYMENT_ID", "gpt-4.1"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=300
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        raise Exception(f"Error generating answer: {str(e)}")
