from pyhocon import ConfigFactory
from abc import ABC
from singleton_decorator import singleton


class BaseConfig(ABC):
    def __init__(self, config):
        self._config = config

    def get(self, key):
        return self._config.get(key)


@singleton
class ConfigService(BaseConfig):
    ref = "./resources/application.conf"

    def __init__(self, config=None):
        if not config:
            super().__init__(ConfigFactory.parse_file(self.ref))
        else:
            super().__init__(config)

    def get_app_config(self):
        return AppConfig(self.get("app-config"))


class AppConfig(BaseConfig):

    @property
    def model_path(self):
        return self.get("model-path")

    def __str__(self):
        return "AppConfig: model_path {1}".format(self.sites, self.model_path)
