from abc import ABC, abstractmethod


class SimilarityModel(ABC):
    @abstractmethod
    def get_similar_items(self, item_id, limit):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def is_ready(self):
        pass
