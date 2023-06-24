from openai_service import OPENAIService
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

class SearchService:
    def __init__(self) -> None:
        self.qdrant_client = QdrantClient(path='./vectordb')
        self.openai_service = OPENAIService()
    

    def search(self,query_str:str,product_name:str):
        query_embedding = self.openai_service.get_embedding(input_text=query_str)
        
        search_result = self.qdrant_client.search(
            collection_name="golfghost",
            query_vector=query_embedding,
            query_filter=Filter(
            must=[FieldCondition(key="product_name",
                                 match=MatchValue(value=product_name)
                                 )
                  ]
            ),
            limit = 10,
        )
        all_results = [dict(result) for result in search_result]
        return all_results

    def search_output(self,query:str,product_name:str):
        search_results = self.search(query_str=query,product_name=product_name)

        reviews_list = []
        for item in search_results:
            review_text = item['payload']['content']
            reviews_list.append(review_text)
        summarize_output = self.openai_service.summarize_text(reviews_list)

        return search_results,summarize_output
