from fastapi import FastAPI
from api import similarity_api
from service.similarity_service import SimilarityService
from model.annoy_model import AnnoyModel
import threading

app = FastAPI()

app.include_router(similarity_api.router, prefix='/similar_items')

def init():
    similarity_model = AnnoyModel()
    similarity_service = SimilarityService(similarity_model)
    similarity_service.warm_up()


init_thread = threading.Thread(target=init)
init_thread.start()
