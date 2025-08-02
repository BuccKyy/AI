#!/usr/bin/env python3
"""
Simple demo cho Pain Point to Solution Agent
Không cần external dependencies
"""

import json
import re
from typing import List, Dict, Any

class SimpleMatcher:
    """Simple matching algorithm không cần external libraries"""
    
    def __init__(self):
        self.features = self._load_features()
    
    def _load_features(self):
        """Load features từ JSON"""
        try:
            with open('data/filum_features.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def simple_similarity(self, text1: str, text2: str) -> float:
        """Tính similarity đơn giản"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def find_solutions(self, pain_point: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Tìm solutions cho pain point"""
        scored_features = []
        
        for feature in self.features:
            # Tính score dựa trên keywords
            keywords = feature.get('keywords', [])
            keyword_score = 0
            for keyword in keywords:
                if keyword.lower() in pain_point.lower():
                    keyword_score += 0.3
            
            # Tính score dựa trên pain points addressed
            pain_points = feature.get('pain_points_addressed', [])
            semantic_score = 0
            for point in pain_points:
                similarity = self.simple_similarity(pain_point, point)
                semantic_score = max(semantic_score, similarity)
            
            # Tổng hợp score
            total_score = (keyword_score * 0.6) + (semantic_score * 0.4)
            
            if total_score > 0.1:
                scored_features.append({
                    'feature': feature,
                    'relevance_score': total_score
                })
        
        # Sắp xếp theo score
        scored_features.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Trả về kết quả
        results = []
        for item in scored_features[:max_results]:
            feature = item['feature']
            relevance_score = item['relevance_score']
            
            solution = {
                'feature_name': feature.get('feature_name', ''),
                'category': f"{feature.get('category', '')} - {feature.get('subcategory', '')}",
                'description': feature.get('description', ''),
                'relevance_score': round(relevance_score, 2),
                'how_it_helps': self._generate_how_it_helps(feature),
                'time_to_implement': feature.get('time_to_value', ''),
                'estimated_impact': self._get_estimated_impact(feature)
            }
            
            results.append(solution)
        
        return results
    
    def _generate_how_it_helps(self, feature: Dict[str, Any]) -> str:
        """Tạo mô tả how it helps"""
        pain_points = feature.get('pain_points_addressed', [])
        if pain_points:
            return f"Addresses: {', '.join(pain_points[:2])}"
        else:
            capabilities = feature.get('key_capabilities', ['automation'])
            return f"Provides {capabilities[0]} to solve your issue"
    
    def _get_estimated_impact(self, feature: Dict[str, Any]) -> str:
        """Lấy estimated impact"""
        success_metrics = feature.get('success_metrics', [])
        if success_metrics:
            return success_metrics[0]
        return "Improve efficiency and customer satisfaction"

def demo_matching():
    """Demo matching process"""
    print("Pain Point to Solution Agent - Simple Demo")
    print("=" * 50)
    
    matcher = SimpleMatcher()
    
    # Test cases
    test_cases = [
        "Our support agents are overwhelmed by repetitive questions",
        "We have no clear idea which customer touchpoints are causing the most frustration",
        "It's difficult to get a single view of a customer's interaction history",
        "Manually analyzing thousands of survey responses is too time-consuming",
        "We struggle to collect customer feedback consistently"
    ]
    
    for i, pain_point in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {pain_point}")
        print(f"{'='*60}")
        
        solutions = matcher.find_solutions(pain_point)
        
        if solutions:
            print(f"\nSUGGESTED SOLUTIONS ({len(solutions)} found):")
            for j, solution in enumerate(solutions, 1):
                print(f"\n{j}. {solution['feature_name']}")
                print(f"   Category: {solution['category']}")
                print(f"   Relevance Score: {solution['relevance_score']}")
                print(f"   How it helps: {solution['how_it_helps']}")
                print(f"   Time to implement: {solution['time_to_implement']}")
                print(f"   Estimated impact: {solution['estimated_impact']}")
        else:
            print("No solutions found.")
        
        print(f"\n{'='*60}")

def interactive_demo():
    """Interactive demo"""
    print("\n" + "="*60)
    print("INTERACTIVE DEMO")
    print("="*60)
    
    matcher = SimpleMatcher()
    
    while True:
        print("\nEnter your pain point (or 'quit' to exit):")
        pain_point = input("> ").strip()
        
        if pain_point.lower() in ['quit', 'exit', 'q']:
            break
        
        if pain_point:
            solutions = matcher.find_solutions(pain_point)
            
            print(f"\nResults for: {pain_point}")
            if solutions:
                for i, solution in enumerate(solutions, 1):
                    print(f"\n{i}. {solution['feature_name']} (Score: {solution['relevance_score']})")
                    print(f"   {solution['how_it_helps']}")
            else:
                print("No solutions found.")
        else:
            print("Please enter a valid pain point.")

def main():
    """Main function"""
    try:
        # Demo với test cases
        demo_matching()
        
        # Interactive demo
        interactive_demo()
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 