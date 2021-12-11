from service.configuration_service import ConfigService
from datetime import datetime
from model.similarity_model import SimilarityModel
from singleton_decorator import singleton


@singleton
class SimilarityService:
   def __init__(self, similarity_model: SimilarityModel = None):
      self.config = ConfigService()
      self.app_config = self.config.get_app_config()
      self.model = similarity_model

   def warm_up(self):
      self.load_model()

   def load_model(self):
      self.model.load()

   def get_similar_items(self, item_id, limit=20):
      start_time = datetime.now()
      related_items = self.model.get_similar_items(item_id, limit)
      time_diff = (datetime.now() - start_time)
      return {"recommendations": related_items, "elasped_time_ms": time_diff}

   def is_ready(self):
      return self.model.is_ready()

   def reload_model(self):
      self.load_model()
