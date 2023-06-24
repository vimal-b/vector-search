# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module
# pylint: disable=missing-module-docstring
from typing import Optional, List, Union
from pydantic import BaseModel, Field, validator


class VectorSearchInputModel(BaseModel):
    """ Input Model for the API"""
    query: str = Field(...,description="Search query")
    product_name:str = Field(..., description="Name of the Product")
    request_id: Optional[str]

    class Config:
        """ Sample Config"""
        schema_extra = {
            "example": {
                "query": "reviews highlighting the packaging issue",
                "product_name":"GHOST WHITE",
                "request_id": "7f420a8c9e464483b7507b826fb96e9d"
            }
        }






class VectorSearchOutputModel(BaseModel):
    """ Output Model for the API"""
    search_results:List
    summarize_output:str 
    request_id: Optional[str]
    response_id: str
    message: str = "Vector Search done Successfully"

    class Config:
        """ Sampel Config"""
        schema_extra = {
            "example": {
                "results": [
                    {
                        "image_url": "https://storage.googleapis.com/etl-video-frames/tiktok_videos/6781041654808759557/frame0.jpg",
                        "is_nsfw": False
                    }
                ],
                "request_id": "7f420a8c9e464483b7507b826fb96e9d",
                "response_id": "f027817d40d74c1daed4b82d662f812b",
                "message": "Image Prediction done Successfully"
            }
        }


class RootModel(BaseModel):
    """ Root Model"""
    message: str

    class Config:
        """ Sample Config"""
        schema_extra = {
            "example": {
                "message": """This REST API will do the vector search and return the summary of reviews"""
            }
        }
