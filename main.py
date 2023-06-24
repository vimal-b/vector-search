#pylint: disable=missing-module-docstring
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import CommaSeparatedStrings
from settings import settings
from route import router as VectorSearchRouter
from model import RootModel

app = FastAPI(title="Vector Search",
              description="""This REST API will do the vector search and return the summary of reviews""",
                          version="1.0",
                          openapi_url="/api/v1/openapi.json")

app.include_router(VectorSearchRouter, prefix=settings.api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CommaSeparatedStrings(settings.allowed_hosts),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"], response_model=RootModel)
async def read_root():
    """ Root End Point to Describe the API"""
    return RootModel(message="""This REST API will do the vector search and return the summary of reviews""")

if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",port=5000,log_level="info")