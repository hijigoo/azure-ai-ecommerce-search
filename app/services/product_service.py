"""
Product Service module.
Provides methods for product management, description generation, and UUID handling.
"""

import json
import uuid
from typing import Dict, Any, Optional, List
from pathlib import Path
from services.openai_service import get_openai_service
from services.vision_service import get_vision_service
from config import Config


class ProductService:
    """Service for product management operations"""
    
    def __init__(self):
        """Initialize product service"""
        self.openai_service = get_openai_service()
        self.vision_service = get_vision_service()
    
    def generate_product_description(
        self,
        product_info: Dict[str, Any],
        length: str = "medium",
        tone: str = "professional"
    ) -> str:
        """
        Generate product description using GPT-4.
        
        Args:
            product_info: Product information dictionary
            length: Description length (short/medium/long)
            tone: Writing tone (casual/professional/luxury)
            
        Returns:
            Generated description text
        """
        length_guide = {
            "short": "2-3문장, 100자 내외",
            "medium": "5-7문장, 200-300자",
            "long": "10문장 이상, 500자 이상"
        }
        
        tone_guide = {
            "casual": "친근하고 편안한 말투",
            "professional": "전문적이고 신뢰감 있는 말투",
            "luxury": "고급스럽고 우아한 말투"
        }
        
        name = product_info.get("name", "상품")
        category = product_info.get("category", "")
        attributes = product_info.get("attributes", {})
        features = product_info.get("features", [])
        
        prompt = f"""
        다음 상품에 대한 매력적인 상세 설명을 작성해주세요.
        
        [상품 정보]
        - 상품명: {name}
        - 카테고리: {category}
        - 색상: {attributes.get('color', 'N/A')}
        - 소재: {attributes.get('material', 'N/A')}
        - 스타일: {attributes.get('style', 'N/A')}
        - 계절: {attributes.get('season', 'N/A')}
        - 특징: {', '.join(features) if features else 'N/A'}
        
        [작성 가이드]
        - 길이: {length_guide.get(length, length_guide['medium'])}
        - 말투: {tone_guide.get(tone, tone_guide['professional'])}
        - 상품의 장점과 활용도를 자연스럽게 강조
        - 구매 욕구를 자극하는 표현 사용
        
        상품 설명만 작성해주세요 (다른 설명 없이):
        """
        
        system_message = "당신은 이커머스 전문 카피라이터입니다. 매력적이고 설득력 있는 상품 설명을 작성합니다."
        
        description = self.openai_service.generate_text(
            prompt=prompt,
            system_message=system_message,
            temperature=0.7
        )
        
        return description.strip()
    
    def create_product_from_image(
        self,
        image_data: str,
        is_url: bool = False,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a complete product entry from an image.
        
        Args:
            image_data: Base64 encoded image or image URL
            is_url: Whether image_data is a URL
            additional_info: Additional product info (brand, price, etc.)
            
        Returns:
            Complete product dictionary or None if failed
        """
        # Validate product image
        is_valid, reason = self.vision_service.validate_product_image(image_data, is_url)
        if not is_valid:
            print(f"이미지 검증 실패: {reason}")
            return None
        
        # Extract attributes from image
        extracted = self.vision_service.extract_product_attributes(image_data, is_url)
        if not extracted:
            print("속성 추출 실패")
            return None
        
        # Generate product description
        description = self.generate_product_description(extracted, length="medium")
        
        # Create complete product object
        product = {
            "id": str(uuid.uuid4()),
            "name": extracted.get("name", "새 상품"),
            "brand": additional_info.get("brand", "일반") if additional_info else "일반",
            "price": additional_info.get("price", 0) if additional_info else 0,
            "category": extracted.get("category", "미분류"),
            "description": description,
            "attributes": extracted.get("attributes", {}),
            "features": extracted.get("features", []),
            "stock": additional_info.get("stock", 100) if additional_info else 100,
            "rating": 0.0,
            "image_url": image_data if is_url else None
        }
        
        return product
    
    def add_embedding_to_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add embedding vector to product.
        
        Args:
            product: Product dictionary
            
        Returns:
            Product with embedding added
        """
        # Create text for embedding
        text_parts = [
            product.get("name", ""),
            product.get("brand", ""),
            product.get("description", ""),
            product.get("category", "")
        ]
        
        # Add attributes
        attributes = product.get("attributes", {})
        for key, value in attributes.items():
            text_parts.append(f"{key}: {value}")
        
        # Add features
        features = product.get("features", [])
        if features:
            text_parts.extend(features)
        
        text = " ".join(filter(None, text_parts))
        
        # Generate embedding
        embedding = self.openai_service.get_embedding(text)
        product["embedding"] = embedding.tolist()
        
        return product
    
    @staticmethod
    def load_products_from_json(file_path: str) -> List[Dict[str, Any]]:
        """
        Load products from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of product dictionaries
        """
        path = Path(file_path)
        if not path.exists():
            return []
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def save_products_to_json(products: List[Dict[str, Any]], file_path: str):
        """
        Save products to JSON file.
        
        Args:
            products: List of product dictionaries
            file_path: Path to JSON file
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)


# Singleton instance
_product_service = None


def get_product_service() -> ProductService:
    """Get or create Product service instance"""
    global _product_service
    if _product_service is None:
        _product_service = ProductService()
    return _product_service
