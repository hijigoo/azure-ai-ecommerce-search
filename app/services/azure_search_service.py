"""
Azure AI Search Service module.
Provides methods for hybrid, semantic, and vector search strategies.
"""

from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from config import Config
from services.openai_service import get_openai_service


class AzureSearchService:
    """Service for Azure AI Search operations"""
    
    def __init__(self):
        """Initialize Azure AI Search client"""
        # Use managed identity authentication
        credential = DefaultAzureCredential()
        
        self.search_client = SearchClient(
            endpoint=Config.AZURE_SEARCH_SERVICE_ENDPOINT,
            index_name=Config.AZURE_SEARCH_INDEX_NAME,
            credential=credential
        )
        
        self.openai_service = get_openai_service()
    
    def get_all_products(
        self,
        top_k: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all products from the index.
        
        Args:
            top_k: Number of results to return
            
        Returns:
            List of all products
        """
        results = self.search_client.search(
            search_text="*",
            select=["id", "name", "brand", "description", "price", "imageUrl", 
                    "imageCaption", "imageDescription", "imageTags"],
            top=top_k
        )
        
        return self._process_results(results)
    
    def keyword_search(
        self,
        query: str,
        search_fields: List[str] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Perform keyword (full-text) search only.
        
        Args:
            query: Search query text
            search_fields: List of fields to search in (None = all searchable fields)
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        top_k = top_k or Config.MAX_SEARCH_RESULTS
        
        search_params = {
            "search_text": query,
            "top": top_k,

            "select": ["id", "name", "brand", "description", "price", 
                      "imageUrl", "imageCaption", "imageDescription", "imageTags"]
        }
        
        # Add search_fields only if specified
        if search_fields:
            search_params["search_fields"] = search_fields
        
        results = self.search_client.search(**search_params)
        return self._process_results(results)
    
    def hybrid_search(
        self,
        query: str,
        search_fields: List[str] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search (keyword + vector).
        
        Args:
            query: Search query text
            search_fields: List of fields to search in (None = all searchable fields)
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        top_k = top_k or Config.MAX_SEARCH_RESULTS
        
        # Generate query embedding
        query_embedding = self.openai_service.get_embedding(query)
        
        # Create vectorized query
        vector_query = VectorizedQuery(
            vector=query_embedding.tolist(),
            k_nearest_neighbors=top_k,
            fields="descriptionVector"
        )
        
        search_params = {
            "search_text": query,
            "vector_queries": [vector_query],
            "select": ["id", "name", "brand", "description", "price", 
                      "imageUrl", "imageCaption", "imageDescription", "imageTags"],
            "top": top_k
        }
        
        # Add search_fields only if specified
        if search_fields:
            search_params["search_fields"] = search_fields
        
        results = self.search_client.search(**search_params)
        return self._process_results(results)
    
    def vector_search(
        self,
        query: str,
        search_fields: List[str] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Perform pure vector search.
        
        Args:
            query: Search query text
            search_fields: List of fields to search in (not used for vector search, but kept for consistency)
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        top_k = top_k or Config.MAX_SEARCH_RESULTS
        
        # Generate query embedding
        query_embedding = self.openai_service.get_embedding(query)
        
        # Create vectorized query
        vector_query = VectorizedQuery(
            vector=query_embedding.tolist(),
            k_nearest_neighbors=top_k,
            fields="descriptionVector"
        )
        
        # Perform pure vector search
        results = self.search_client.search(
            search_text=None,
            vector_queries=[vector_query],
            select=["id", "name", "brand", "description", "price", 
                   "imageUrl", "imageCaption", "imageDescription", "imageTags"],
            top=top_k
        )
        
        return self._process_results(results)
    
    def upload_product(self, product: Dict[str, Any]) -> bool:
        """
        Upload a single product to Azure AI Search.
        
        Args:
            product: Product dictionary with all fields
            
        Returns:
            True if successful
        """
        try:
            result = self.search_client.upload_documents(documents=[product])
            return result[0].succeeded
        except Exception as e:
            print(f"Error uploading product: {e}")
            return False
    
    def upload_products(self, products: List[Dict[str, Any]]) -> int:
        """
        Upload multiple products to Azure AI Search.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Number of successfully uploaded products
        """
        try:
            results = self.search_client.upload_documents(documents=products)
            success_count = sum(1 for r in results if r.succeeded)
            return success_count
        except Exception as e:
            print(f"Error uploading products: {e}")
            return 0
    
    def _process_results(self, results) -> List[Dict[str, Any]]:
        """
        Process search results into a list of dictionaries.
        
        Args:
            results: Raw search results
            
        Returns:
            Processed list of product dictionaries
        """
        products = []
        for result in results:
            product = {
                "id": result.get("id"),
                "name": result.get("name"),
                "brand": result.get("brand"),
                "description": result.get("description"),
                "price": result.get("price"),
                "imageUrl": result.get("imageUrl"),
                "imageCaption": result.get("imageCaption"),
                "imageDescription": result.get("imageDescription"),
                "imageTags": result.get("imageTags", []),
                "score": getattr(result, "@search.score", None),
                "reranker_score": getattr(result, "@search.reranker_score", None)
            }
            products.append(product)
        
        return products


# Singleton instance
_search_service = None


def get_search_service() -> AzureSearchService:
    """Get or create Azure Search service instance"""
    global _search_service
    if _search_service is None:
        _search_service = AzureSearchService()
    return _search_service
