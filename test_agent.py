#!/usr/bin/env python3
"""
Test script cho Pain Point to Solution Agent
"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agent import PainPointToSolutionAgent
from utils import load_test_cases, run_batch_test, calculate_performance_metrics

def test_single_case():
    """Test với một case đơn giản"""
    print("Testing single case...")
    
    agent = PainPointToSolutionAgent()
    
    input_data = {
        "pain_point": "Our support agents are overwhelmed by repetitive questions",
        "business_context": {
            "industry": "e-commerce",
            "company_size": "medium",
            "customer_volume": "high"
        }
    }
    
    result = agent.process_input(input_data)
    
    print(f"Input: {input_data['pain_point']}")
    print(f"Confidence Score: {result['confidence_score']}")
    
    if result['suggested_solutions']:
        top_solution = result['suggested_solutions'][0]
        print(f"Top Solution: {top_solution['feature_name']}")
        print(f"Relevance Score: {top_solution['relevance_score']}")
    else:
        print("No solutions found")

def test_batch_cases():
    """Test với batch cases"""
    print("\n" + "="*60)
    print("BATCH TESTING")
    print("="*60)
    
    agent = PainPointToSolutionAgent()
    test_cases = load_test_cases()
    
    results = run_batch_test(agent, test_cases)
    
    # Tính performance metrics
    metrics = calculate_performance_metrics(results)
    
    print(f"\nPERFORMANCE METRICS:")
    print(f"Total tests: {metrics['total_tests']}")
    print(f"Successful matches: {metrics['successful_matches']}")
    print(f"Match rate: {metrics['match_rate']:.2%}")
    print(f"Average confidence: {metrics['avg_confidence']:.2f}")
    print(f"Average relevance: {metrics['avg_relevance']:.2f}")

def test_custom_input():
    """Test với custom input"""
    print("\n" + "="*60)
    print("CUSTOM INPUT TEST")
    print("="*60)
    
    agent = PainPointToSolutionAgent()
    
    # Test cases từ examples
    custom_cases = [
        {
            "pain_point": "We have no clear idea which customer touchpoints are causing the most frustration",
            "business_context": {
                "industry": "retail",
                "company_size": "large",
                "customer_volume": "very_high"
            }
        },
        {
            "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us",
            "business_context": {
                "industry": "financial_services",
                "company_size": "large",
                "customer_volume": "high"
            }
        },
        {
            "pain_point": "Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming",
            "business_context": {
                "industry": "technology",
                "company_size": "medium",
                "customer_volume": "medium"
            }
        }
    ]
    
    for i, case in enumerate(custom_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Pain Point: {case['pain_point']}")
        
        result = agent.process_input(case)
        
        print(f"Confidence Score: {result['confidence_score']}")
        
        if result['suggested_solutions']:
            for j, solution in enumerate(result['suggested_solutions'][:2], 1):
                print(f"  {j}. {solution['feature_name']} (Score: {solution['relevance_score']})")
        else:
            print("  No solutions found")

def test_feature_statistics():
    """Test feature statistics"""
    print("\n" + "="*60)
    print("FEATURE STATISTICS")
    print("="*60)
    
    agent = PainPointToSolutionAgent()
    stats = agent.get_feature_statistics()
    
    print(f"Total features: {stats['total_features']}")
    print(f"\nCategories:")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count}")
    
    print(f"\nComplexities:")
    for complexity, count in stats['complexities'].items():
        print(f"  {complexity}: {count}")

def main():
    """Main test function"""
    print("Pain Point to Solution Agent - Test Suite")
    print("=" * 50)
    
    try:
        # Test single case
        test_single_case()
        
        # Test batch cases
        test_batch_cases()
        
        # Test custom input
        test_custom_input()
        
        # Test feature statistics
        test_feature_statistics()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 