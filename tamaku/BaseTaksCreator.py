from abc import abstractmethod

from tamaku.utils.Utils import write_json_file


class BaseTaskCreator:
    def __init__(self, config_path: str, registry_url: str):
        self.config_path = config_path
        self.registry_url = registry_url
        self.providers = []
        self.config = self.load_config()

    @abstractmethod
    def load_config(self):
        pass

    @abstractmethod
    def create_tasks(self):
        pass

    def create_tasks_json(self, file_path) -> str:
        tasks = self.create_tasks()
        return write_json_file(file_path, tasks)
