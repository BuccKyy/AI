import json
import os
from typing import List, Dict, Any

class KnowledgeBase:
    """Quản lý knowledge base của các tính năng Filum.ai"""
    
    def __init__(self, features_file: str = "data/filum_features.json"):
        self.features_file = features_file
        self.features = self._load_features()
    
    def _load_features(self) -> List[Dict[str, Any]]:
        """Load features từ JSON file"""
        try:
            with open(self.features_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Features file {self.features_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.features_file}")
            return []
    
    def get_all_features(self) -> List[Dict[str, Any]]:
        """Lấy tất cả features"""
        return self.features
    
    def get_feature_by_id(self, feature_id: str) -> Dict[str, Any]:
        """Lấy feature theo ID"""
        for feature in self.features:
            if feature.get('feature_id') == feature_id:
                return feature
        return {}
    
    def get_features_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Lấy features theo category"""
        return [f for f in self.features if f.get('category') == category]
    
    def get_features_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Lấy features có chứa keywords"""
        matching_features = []
        for feature in self.features:
            feature_keywords = feature.get('keywords', [])
            if any(keyword.lower() in [k.lower() for k in feature_keywords] for keyword in keywords):
                matching_features.append(feature)
        return matching_features
    
    def search_features(self, query: str) -> List[Dict[str, Any]]:
        """Tìm kiếm features theo query"""
        query_lower = query.lower()
        matching_features = []
        
        for feature in self.features:
            # Tìm trong feature name
            if query_lower in feature.get('feature_name', '').lower():
                matching_features.append(feature)
                continue
            
            # Tìm trong description
            if query_lower in feature.get('description', '').lower():
                matching_features.append(feature)
                continue
            
            # Tìm trong keywords
            keywords = feature.get('keywords', [])
            if any(query_lower in keyword.lower() for keyword in keywords):
                matching_features.append(feature)
                continue
            
            # Tìm trong pain points addressed
            pain_points = feature.get('pain_points_addressed', [])
            if any(query_lower in point.lower() for point in pain_points):
                matching_features.append(feature)
        
        return matching_features
    
    def get_feature_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về features"""
        categories = {}
        complexities = {}
        
        for feature in self.features:
            category = feature.get('category', 'Unknown')
            complexity = feature.get('implementation_complexity', 'Unknown')
            
            categories[category] = categories.get(category, 0) + 1
            complexities[complexity] = complexities.get(complexity, 0) + 1
        
        return {
            'total_features': len(self.features),
            'categories': categories,
            'complexities': complexities
        } 