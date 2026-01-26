#!/usr/bin/env python3
"""
AI Evals CI Pipeline Script

Runs automated evaluations on test cases and exits with appropriate code for CI/CD
"""

import json
import sys
import os
import requests
from evaluators.deterministic import run_deterministic_evals
from evaluators.llm_judge import run_llm_judge, passed_threshold

# Configuration
USE_API_MODE = os.getenv("USE_API_MODE", "false").lower() == "true"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def load_test_cases(filepath: str = "test_cases.json") -> list:
    """Load test cases from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading test cases: {e}")
        sys.exit(1)


def generate_answer_via_api(user_message: str, expected_language: str = None) -> str:
    """
    Call the API endpoint to get AI response
    
    Args:
        user_message: User's input message
        expected_language: Expected language code
        
    Returns:
        AI-generated response
    """
    try:
        url = f"{API_BASE_URL}/chat"
        payload = {"message": user_message}
        if expected_language:
            payload["expected_language"] = expected_language
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["answer"]
    except Exception as e:
        raise Exception(f"API call failed: {str(e)}")


def generate_answer_direct(user_message: str) -> str:
    """
    Call LLM directly (for local development)
    
    Args:
        user_message: User's input message
        
    Returns:
        AI-generated response
    """
    from llm_client import generate_answer
    return generate_answer(user_message)


def run_evaluation(case_input: str, expected_language: str = None) -> dict:
    """
    Run full evaluation pipeline for a single test case
    
    Args:
        case_input: User input message
        expected_language: Expected language code ('es' or 'en')
    
    Returns:
        Dictionary with answer, evaluations, and pass/fail status
    """
    try:
        # Generate AI answer (via API or direct)
        if USE_API_MODE:
            ai_answer = generate_answer_via_api(case_input, expected_language)
        else:
            ai_answer = generate_answer_direct(case_input)
        
        # Run deterministic evaluations
        deterministic_results = run_deterministic_evals(ai_answer, expected_language)
        
        # Run LLM judge
        llm_judge_results = run_llm_judge(case_input, ai_answer)
        
        # Check if passed
        all_deterministic_passed = all(deterministic_results.values())
        llm_passed = passed_threshold(llm_judge_results)
        passed = all_deterministic_passed and llm_passed
        
        # Identify failure reasons
        failure_reasons = []
        if not all_deterministic_passed:
            failed_checks = [k for k, v in deterministic_results.items() if not v]
            failure_reasons.extend([f"deterministic: {check}" for check in failed_checks])
        if not llm_passed:
            for criterion in ["empathy", "clarity"]:
                if criterion == "empathy" and llm_judge_results.get("empathy", 0) < 3.5:
                    failure_reasons.append("low empathy")
                elif criterion == "clarity" and llm_judge_results.get("clarity", 0) < 3.0:
                    failure_reasons.append("low clarity")
        
        return {
            "input": case_input,
            "answer": ai_answer,
            "deterministic": deterministic_results,
            "llm_judge": llm_judge_results,
            "passed": passed,
            "failure_reasons": failure_reasons
        }
        
    except Exception as e:
        return {
            "input": case_input,
            "error": str(e),
            "passed": False,
            "failure_reasons": [f"error: {str(e)}"]
        }


def print_report(results: list):
    """Print evaluation report to console"""
    print("\n" + "="*80)
    print("AI EVALS REPORT")
    print("="*80 + "\n")
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"CASE {i}: {status}")
        print(f"  Input: {result['input']}")
        
        if not result["passed"]:
            print(f"  Reasons: {', '.join(result['failure_reasons'])}")
        
        if "answer" in result:
            print(f"  Answer: {result['answer']}")
            print(f"  Deterministic: {result['deterministic']}")
            print(f"  LLM Judge: {result['llm_judge']}")
        
        print()
    
    print("="*80)
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    print(f"FINAL RESULT: {passed_count}/{total_count} PASSED")
    
    if passed_count == total_count:
        print("✅ ALL TESTS PASSED")
        print("="*80 + "\n")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("="*80 + "\n")
        return False


def main():
    """Main execution function"""
    print("🚀 Starting AI Evals Pipeline...\n")
    
    # Show execution mode
    if USE_API_MODE:
        print(f"📡 API Mode: Testing against {API_BASE_URL}")
    else:
        print("💻 Direct Mode: Testing with local LLM client")
    print()
    
    # Load test cases
    test_cases = load_test_cases()
    print(f"📋 Loaded {len(test_cases)} test cases\n")
    
    # Run evaluations
    results = []
    for i, case in enumerate(test_cases, 1):
        print(f"⚙️  Processing case {i}/{len(test_cases)}...")
        case_input = case.get("input", "")
        expected_language = case.get("expected_language")
        result = run_evaluation(case_input, expected_language)
        results.append(result)
    
    # Print report
    all_passed = print_report(results)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
