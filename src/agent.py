import json
import sys
import os
from typing import Dict, Any, List

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge_base import KnowledgeBase
from matcher import PainPointMatcher

class PainPointToSolutionAgent:
    """Main Agent class cho Pain Point to Solution matching"""
    
    def __init__(self, features_file: str = "data/filum_features.json"):
        self.knowledge_base = KnowledgeBase(features_file)
        self.matcher = PainPointMatcher(self.knowledge_base)
    
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Xử lý input và trả về output"""
        pain_point = input_data.get('pain_point', '')
        business_context = input_data.get('business_context', {})
        
        if not pain_point:
            return {
                'error': 'Pain point is required',
                'suggested_solutions': [],
                'confidence_score': 0.0
            }
        
        # Tìm solutions
        solutions = self.matcher.find_solutions(pain_point, business_context)
        
        # Tính confidence score
        confidence_score = self.matcher.calculate_confidence_score(solutions)
        
        # Tạo alternative approaches
        alternative_approaches = self._generate_alternative_approaches(pain_point)
        
        # Tạo next steps
        next_steps = self._generate_next_steps(solutions, business_context)
        
        return {
            'suggested_solutions': solutions,
            'confidence_score': round(confidence_score, 2),
            'alternative_approaches': alternative_approaches,
            'next_steps': next_steps
        }
    
    def _generate_alternative_approaches(self, pain_point: str) -> List[str]:
        """Tạo alternative approaches"""
        alternatives = [
            "Consider manual process improvements first",
            "Implement basic automation tools",
            "Hire additional staff for immediate relief",
            "Use existing tools more effectively"
        ]
        return alternatives[:3]
    
    def _generate_next_steps(self, solutions: List[Dict[str, Any]], business_context: Dict[str, Any]) -> List[str]:
        """Tạo next steps dựa trên solutions"""
        next_steps = []
        
        if solutions:
            # Next steps dựa trên solution đầu tiên
            top_solution = solutions[0]
            next_steps.extend([
                f"Schedule demo of {top_solution['feature_name']}",
                "Review implementation timeline and requirements",
                "Prepare training materials for team"
            ])
        
        # Thêm next steps chung
        next_steps.extend([
            "Conduct pilot program with small team",
            "Measure current baseline metrics",
            "Set up success measurement framework"
        ])
        
        return next_steps[:5]
    
    def get_feature_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về features"""
        return self.knowledge_base.get_feature_statistics()
    
    def demo_matching(self, pain_point: str, business_context: Dict[str, Any] = None) -> None:
        """Demo matching process"""
        print(f"\n{'='*60}")
        print(f"PAIN POINT: {pain_point}")
        print(f"{'='*60}")
        
        if business_context:
            print(f"Business Context: {json.dumps(business_context, indent=2)}")
        
        result = self.process_input({
            'pain_point': pain_point,
            'business_context': business_context or {}
        })
        
        print(f"\nCONFIDENCE SCORE: {result['confidence_score']}")
        print(f"\nSUGGESTED SOLUTIONS:")
        
        for i, solution in enumerate(result['suggested_solutions'], 1):
            print(f"\n{i}. {solution['feature_name']}")
            print(f"   Category: {solution['category']}")
            print(f"   Relevance Score: {solution['relevance_score']}")
            print(f"   How it helps: {solution['how_it_helps']}")
            print(f"   Time to implement: {solution['time_to_implement']}")
            print(f"   Estimated impact: {solution['estimated_impact']}")
        
        if result['alternative_approaches']:
            print(f"\nALTERNATIVE APPROACHES:")
            for approach in result['alternative_approaches']:
                print(f"   • {approach}")
        
        if result['next_steps']:
            print(f"\nNEXT STEPS:")
            for step in result['next_steps']:
                print(f"   • {step}")
        
        print(f"\n{'='*60}")

def load_examples():
    """Load examples từ files"""
    try:
        with open('examples/input_examples.json', 'r', encoding='utf-8') as f:
            input_examples = json.load(f)
        
        with open('examples/output_examples.json', 'r', encoding='utf-8') as f:
            output_examples = json.load(f)
        
        return input_examples, output_examples
    except FileNotFoundError:
        print("Warning: Example files not found")
        return [], []

def main():
    """Main function để chạy demo"""
    print("Pain Point to Solution Agent - Filum.ai")
    print("=" * 50)
    
    # Khởi tạo agent
    agent = PainPointToSolutionAgent()
    
    # Load examples
    input_examples, output_examples = load_examples()
    
    # Hiển thị thống kê
    stats = agent.get_feature_statistics()
    print(f"\nKnowledge Base Statistics:")
    print(f"Total features: {stats['total_features']}")
    print(f"Categories: {stats['categories']}")
    print(f"Complexities: {stats['complexities']}")
    
    # Demo với examples
    if input_examples:
        print(f"\n{'='*60}")
        print("DEMO WITH EXAMPLE PAIN POINTS")
        print(f"{'='*60}")
        
        for i, example in enumerate(input_examples[:3], 1):  # Chỉ demo 3 examples đầu
            pain_point = example['pain_point']
            business_context = example.get('business_context', {})
            
            print(f"\nExample {i}:")
            agent.demo_matching(pain_point, business_context)
    
    # Interactive demo
    print(f"\n{'='*60}")
    print("INTERACTIVE DEMO")
    print(f"{'='*60}")
    
    while True:
        print("\nEnter your pain point (or 'quit' to exit):")
        pain_point = input("> ").strip()
        
        if pain_point.lower() in ['quit', 'exit', 'q']:
            break
        
        if pain_point:
            agent.demo_matching(pain_point)
        else:
            print("Please enter a valid pain point.")

if __name__ == "__main__":
    main() 