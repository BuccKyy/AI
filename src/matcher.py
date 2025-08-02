import re
from typing import List, Dict, Any, Tuple
from fuzzywuzzy import fuzz
from knowledge_base import KnowledgeBase

class PainPointMatcher:
    """Thực hiện matching giữa pain points và Filum.ai features"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        
    def extract_keywords(self, text: str) -> List[str]:
        """Trích xuất keywords từ text"""
        # Loại bỏ các từ không quan trọng
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'we', 'our', 'us', 'they', 'them', 'their'}
        
        # Tách từ và loại bỏ punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Loại bỏ stop words và từ ngắn
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def calculate_keyword_score(self, pain_point: str, feature: Dict[str, Any]) -> float:
        """Tính điểm keyword matching"""
        pain_keywords = self.extract_keywords(pain_point)
        feature_keywords = feature.get('keywords', [])
        
        if not pain_keywords or not feature_keywords:
            return 0.0
        
        # Tính similarity cho từng keyword
        total_score = 0
        for pain_keyword in pain_keywords:
            max_similarity = 0
            for feature_keyword in feature_keywords:
                similarity = fuzz.ratio(pain_keyword.lower(), feature_keyword.lower()) / 100.0
                max_similarity = max(max_similarity, similarity)
            total_score += max_similarity
        
        return total_score / len(pain_keywords)
    
    def calculate_semantic_score(self, pain_point: str, feature: Dict[str, Any]) -> float:
        """Tính điểm semantic similarity"""
        # So sánh với pain points addressed
        pain_points_addressed = feature.get('pain_points_addressed', [])
        max_similarity = 0
        
        for addressed_point in pain_points_addressed:
            similarity = fuzz.ratio(pain_point.lower(), addressed_point.lower()) / 100.0
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def calculate_context_score(self, business_context: Dict[str, Any], feature: Dict[str, Any]) -> float:
        """Tính điểm context relevance"""
        score = 0.5  # Base score
        
        # Kiểm tra industry relevance
        industry = business_context.get('industry', '').lower()
        use_cases = [case.lower() for case in feature.get('use_cases', [])]
        
        if industry and any(industry in case for case in use_cases):
            score += 0.3
        
        # Kiểm tra company size vs implementation complexity
        company_size = business_context.get('company_size', '').lower()
        complexity = feature.get('implementation_complexity', '').lower()
        
        if company_size == 'small' and complexity == 'low':
            score += 0.2
        elif company_size == 'medium' and complexity in ['low', 'medium']:
            score += 0.2
        elif company_size == 'large' and complexity in ['medium', 'high']:
            score += 0.2
        
        return min(score, 1.0)
    
    def calculate_feasibility_score(self, business_context: Dict[str, Any], feature: Dict[str, Any]) -> float:
        """Tính điểm implementation feasibility"""
        score = 0.5  # Base score
        
        # Kiểm tra budget constraints
        budget = business_context.get('budget_constraints', '').lower()
        complexity = feature.get('implementation_complexity', '').lower()
        
        if budget == 'low' and complexity == 'low':
            score += 0.3
        elif budget == 'moderate' and complexity in ['low', 'medium']:
            score += 0.3
        elif budget == 'high' and complexity in ['medium', 'high']:
            score += 0.3
        elif budget == 'flexible':
            score += 0.2
        
        # Kiểm tra urgency
        urgency = business_context.get('urgency_level', '').lower()
        time_to_value = feature.get('time_to_value', '')
        
        if urgency == 'high' and '1-2 weeks' in time_to_value:
            score += 0.2
        elif urgency == 'medium' and '2-4 weeks' in time_to_value:
            score += 0.2
        
        return min(score, 1.0)
    
    def calculate_relevance_score(self, pain_point: str, business_context: Dict[str, Any], feature: Dict[str, Any]) -> float:
        """Tính điểm relevance tổng hợp"""
        keyword_score = self.calculate_keyword_score(pain_point, feature)
        semantic_score = self.calculate_semantic_score(pain_point, feature)
        context_score = self.calculate_context_score(business_context, feature)
        feasibility_score = self.calculate_feasibility_score(business_context, feature)
        
        # Weighted scoring
        relevance_score = (keyword_score * 0.4) + \
                         (semantic_score * 0.35) + \
                         (context_score * 0.15) + \
                         (feasibility_score * 0.1)
        
        return min(relevance_score, 1.0)
    
    def find_solutions(self, pain_point: str, business_context: Dict[str, Any] = None, max_results: int = 3) -> List[Dict[str, Any]]:
        """Tìm solutions cho pain point"""
        if business_context is None:
            business_context = {}
        
        all_features = self.kb.get_all_features()
        scored_features = []
        
        for feature in all_features:
            relevance_score = self.calculate_relevance_score(pain_point, business_context, feature)
            
            if relevance_score > 0.1:  # Chỉ lấy những features có relevance > 10%
                scored_features.append({
                    'feature': feature,
                    'relevance_score': relevance_score
                })
        
        # Sắp xếp theo relevance score
        scored_features.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Trả về top results
        results = []
        for item in scored_features[:max_results]:
            feature = item['feature']
            relevance_score = item['relevance_score']
            
            solution = {
                'feature_name': feature.get('feature_name', ''),
                'category': f"{feature.get('category', '')} - {feature.get('subcategory', '')}",
                'description': feature.get('description', ''),
                'relevance_score': round(relevance_score, 2),
                'how_it_helps': self._generate_how_it_helps(pain_point, feature),
                'implementation_steps': feature.get('integration_requirements', []),
                'estimated_impact': self._get_estimated_impact(feature),
                'time_to_implement': feature.get('time_to_value', '')
            }
            
            results.append(solution)
        
        return results
    
    def _generate_how_it_helps(self, pain_point: str, feature: Dict[str, Any]) -> str:
        """Tạo mô tả how it helps"""
        pain_points_addressed = feature.get('pain_points_addressed', [])
        if pain_points_addressed:
            return f"Addresses: {', '.join(pain_points_addressed[:2])}"
        else:
            return f"Provides {feature.get('key_capabilities', ['automation'])[0]} to solve your issue"
    
    def _get_estimated_impact(self, feature: Dict[str, Any]) -> str:
        """Lấy estimated impact từ success metrics"""
        success_metrics = feature.get('success_metrics', [])
        if success_metrics:
            return success_metrics[0]
        return "Improve efficiency and customer satisfaction"
    
    def calculate_confidence_score(self, solutions: List[Dict[str, Any]]) -> float:
        """Tính confidence score tổng thể"""
        if not solutions:
            return 0.0
        
        relevance_scores = [s['relevance_score'] for s in solutions]
        avg_score = sum(relevance_scores) / len(relevance_scores)
        
        # Tính standard deviation để đánh giá consistency
        variance = sum((score - avg_score) ** 2 for score in relevance_scores) / len(relevance_scores)
        std_dev = variance ** 0.5
        
        # Confidence giảm nếu có độ lệch cao
        confidence = avg_score * (1 - std_dev)
        
        return max(0.0, min(1.0, confidence)) 