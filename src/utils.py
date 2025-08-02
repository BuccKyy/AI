import json
import os
from typing import Dict, Any, List

def validate_input_format(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input format"""
    errors = []
    
    # Kiểm tra pain_point
    if 'pain_point' not in input_data or not input_data['pain_point']:
        errors.append("Pain point is required")
    
    # Kiểm tra business_context nếu có
    if 'business_context' in input_data:
        context = input_data['business_context']
        if not isinstance(context, dict):
            errors.append("Business context must be a dictionary")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }

def format_output(output_data: Dict[str, Any]) -> str:
    """Format output thành string đẹp"""
    result = []
    
    # Header
    result.append("=" * 60)
    result.append("PAIN POINT TO SOLUTION AGENT - RESULTS")
    result.append("=" * 60)
    
    # Confidence score
    confidence = output_data.get('confidence_score', 0)
    result.append(f"\nConfidence Score: {confidence}")
    
    # Solutions
    solutions = output_data.get('suggested_solutions', [])
    if solutions:
        result.append(f"\nSUGGESTED SOLUTIONS ({len(solutions)} found):")
        for i, solution in enumerate(solutions, 1):
            result.append(f"\n{i}. {solution['feature_name']}")
            result.append(f"   Category: {solution['category']}")
            result.append(f"   Relevance Score: {solution['relevance_score']}")
            result.append(f"   How it helps: {solution['how_it_helps']}")
            result.append(f"   Time to implement: {solution['time_to_implement']}")
            result.append(f"   Estimated impact: {solution['estimated_impact']}")
    else:
        result.append("\nNo solutions found.")
    
    # Alternative approaches
    alternatives = output_data.get('alternative_approaches', [])
    if alternatives:
        result.append(f"\nALTERNATIVE APPROACHES:")
        for approach in alternatives:
            result.append(f"   • {approach}")
    
    # Next steps
    next_steps = output_data.get('next_steps', [])
    if next_steps:
        result.append(f"\nNEXT STEPS:")
        for step in next_steps:
            result.append(f"   • {step}")
    
    result.append("\n" + "=" * 60)
    
    return "\n".join(result)

def save_result_to_file(result: Dict[str, Any], filename: str = "result.json"):
    """Lưu kết quả vào file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Result saved to {filename}")
    except Exception as e:
        print(f"Error saving result: {e}")

def load_test_cases() -> List[Dict[str, Any]]:
    """Load test cases từ file"""
    test_cases = [
        {
            "pain_point": "Our support agents are overwhelmed by repetitive questions",
            "business_context": {
                "industry": "e-commerce",
                "company_size": "medium",
                "customer_volume": "high"
            }
        },
        {
            "pain_point": "We can't track customer satisfaction across different channels",
            "business_context": {
                "industry": "retail",
                "company_size": "large",
                "customer_volume": "very_high"
            }
        },
        {
            "pain_point": "Manual data entry is taking too much time",
            "business_context": {
                "industry": "technology",
                "company_size": "small",
                "customer_volume": "medium"
            }
        }
    ]
    return test_cases

def run_batch_test(agent, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Chạy batch test với multiple test cases"""
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['pain_point']}")
        result = agent.process_input(test_case)
        results.append({
            'test_case': test_case,
            'result': result
        })
        
        # Hiển thị kết quả ngắn gọn
        solutions = result.get('suggested_solutions', [])
        if solutions:
            print(f"  Top solution: {solutions[0]['feature_name']} (Score: {solutions[0]['relevance_score']})")
        else:
            print("  No solutions found")
    
    return results

def calculate_performance_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Tính performance metrics cho batch test"""
    total_tests = len(results)
    successful_matches = 0
    avg_confidence = 0
    avg_relevance = 0
    
    for result in results:
        solutions = result['result'].get('suggested_solutions', [])
        if solutions:
            successful_matches += 1
            avg_relevance += solutions[0]['relevance_score']
        
        avg_confidence += result['result'].get('confidence_score', 0)
    
    if total_tests > 0:
        avg_confidence /= total_tests
        if successful_matches > 0:
            avg_relevance /= successful_matches
    
    return {
        'total_tests': total_tests,
        'successful_matches': successful_matches,
        'match_rate': successful_matches / total_tests if total_tests > 0 else 0,
        'avg_confidence': avg_confidence,
        'avg_relevance': avg_relevance
    } 