import re


def check_apology(text: str) -> bool:
    """
    Check if the response contains an apology or empathetic acknowledgment
    
    Args:
        text: AI response text
        
    Returns:
        True if apology/empathy is present
    """
    apology_patterns = [
        r'\blo siento\b',
        r'\bdisculpa\b',
        r'\blamento\b',
        r'\bsentimos\b',
        r'\bsorry\b',
        r'\bapologize\b',
        r'\bunderstand.*frustrat',
        r'\bcomprendo\b',
        r'\bentiendo\b'
    ]
    
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in apology_patterns)


def check_escalation_offer(text: str) -> bool:
    """
    Check if the response offers escalation to human support
    
    Args:
        text: AI response text
        
    Returns:
        True if escalation is offered
    """
    escalation_patterns = [
        r'\bequipo\b.*\bespecializado\b',
        r'\bcontactar\b.*\bsoporte\b',
        r'\btransferir\b',
        r'\bescalar\b',
        r'\bagente\b.*\bhumano\b',
        r'\bmanager\b',
        r'\bsupervisor\b',
        r'\brepresentante\b',
        r'\bespecialista\b',
        r'\bcontact.*support\b',
        r'\btransfer.*team\b'
    ]
    
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in escalation_patterns)


def check_no_pii(text: str) -> bool:
    """
    Check that the response doesn't request or expose PII
    
    Args:
        text: AI response text
        
    Returns:
        True if no PII is requested/exposed
    """
    pii_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{16}\b',  # Credit card
        r'\bpassword\b',
        r'\bcontraseña\b',
        r'\bcvv\b',
        r'\bpin\b',
        r'\bnúmero.*tarjeta\b',
        r'\bnumber.*credit\b',
        r'\bsocial.*security\b'
    ]
    
    text_lower = text.lower()
    return not any(re.search(pattern, text_lower) for pattern in pii_patterns)


def check_max_length(text: str, max_words: int = 200) -> bool:
    """
    Check if response is within word limit
    
    Args:
        text: AI response text
        max_words: Maximum allowed words
        
    Returns:
        True if within limit
    """
    word_count = len(text.split())
    return word_count <= max_words


def run_deterministic_evals(text: str) -> dict:
    """
    Run all deterministic evaluations
    
    Args:
        text: AI response text
        
    Returns:
        Dictionary with evaluation results
    """
    return {
        "apology_present": check_apology(text),
        "escalation_offer": check_escalation_offer(text),
        "no_pii": check_no_pii(text),
        "max_length": check_max_length(text)
    }
