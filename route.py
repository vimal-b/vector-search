#pylint: disable=missing-module-docstring
import uuid
from fastapi import APIRouter, Body,HTTPException
from model import VectorSearchInputModel,VectorSearchOutputModel
from loguru import logger
from similarity_search import SearchService

router = APIRouter()
search_service = SearchService()

@router.post("/search-reviews", response_description="Vector Search Done Successfully",
            response_model=VectorSearchOutputModel)
async def search_reviews(input:VectorSearchInputModel = Body(...)):
    """ API End point to search for similar results"""
    response_id = uuid.uuid4().hex
    try:
        logger.info("Vector Search Started")

        output = search_service.search_output(input.query,input.product_name)
        logger.info("Vector Search Ended")
        return VectorSearchOutputModel(search_results = output[0],
                                      summarize_output = output[1],
                                 request_id=input.request_id,
                                 response_id=response_id)
    except Exception as error_response:
        logger.error(f"Error in Vector Search: {str(error_response)}")
        raise HTTPException(status_code=500,
                            detail="Error in Vector Search."+str(error_response)) from error_response