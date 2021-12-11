from model.similarity_model import SimilarityModel
from annoy import AnnoyIndex
import os
import operator
import numpy as np
from service.configuration_service import ConfigService, AppConfig


class AnnoyModel(SimilarityModel):
    app_config: AppConfig = ConfigService().get_app_config()
    min_raw_score = 0.0 # TODO: This dim should be loaded from a config file

    def __init__(self):
        self.init = False
        self.model_path = self.app_config.model_path

    def load(self):
        self.__load_annoy()
        self.init = True

    def is_ready(self):
        return self.init

    def get_similar_items(self, item_id, limit=20):
        print("Preprocessing item")
        processed_item_id = self.preprocess(item_id)
        if processed_item_id is not None:
            print("Querying annoy")
            similar_ids_with_score = self.query_by_index(processed_item_id, limit=limit)
            print("Postprocessing ...")
            similar_items = self.postprocessing(similar_ids_with_score)
            return similar_items
        else:
            return None

    def __load_annoy(self):
        if os.path.exists(self.model_path):
            print("Loading Annoy model %s" % self.model_path)
            dim = 40
            self.nns_model = AnnoyIndex(dim, metric='angular')  # TODO: This params should be loaded from a config file
            self.nns_model.load(self.model_path)
            print("Model loaded successfully for path %s" % self.model_path)
        else:
            print("Annoy index could not be loaded")

    def preprocess(self, item_id):
        return int(item_id)

    def query_by_index(self, item_encoder, limit=20):
        items, dists = self.nns_model.get_nns_by_item(
            item_encoder,
            n=limit,
            search_k=5,  # TODO: This dim should be loaded from a config file
            include_distances=True)

        similar_dict = {idx: distance for idx, distance in zip(items, 1 - np.square(dists) / 2)}

        return sorted(similar_dict.items(),
                      key=operator.itemgetter(1),
                      reverse=True)[1:]

    def postprocessing(self, similar_ids_with_score):
        return self._min_raw_score_filter(similar_ids_with_score)

    def _min_raw_score_filter(self, similar_ids_with_score):
        return [item_id for item_id, score in similar_ids_with_score if score > self.min_raw_score]
