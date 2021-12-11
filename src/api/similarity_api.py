from fastapi import APIRouter, HTTPException
from service.similarity_service import SimilarityService
from fastapi import FastAPI, status, Response
from service.configuration_service import ConfigService

router = APIRouter()
config = ConfigService()

@router.get('/{item_id}')
def similar_items(item_id, response: Response, limit: int = 10):
   similarity_service = SimilarityService()
   return similarity_service.get_similar_items(item_id, limit)
   try:
      similarity_service = similarity_service()
      return similarity_service.get_similar_items(item_id, limit)
   except:
      response.status_code = status.HTTP_404_NOT_FOUND
      return {"status":"error"}

@router.get('/reload/annoy',status_code=status.HTTP_200_OK)
def reload(response: Response):
   try:
      similarity_service = SimilarityService()
      similarity_service.reload_model()
      return {"status": "ok"}
   except:
      response.status_code = status.HTTP_404_NOT_FOUND
      return {"status": "error"}
