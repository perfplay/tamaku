from tamaku.utils.Logger import Logger
from tamaku.tf.TfTaskCreator import TfTaskCreator

logger = Logger()


def main():
    task_creator = TfTaskCreator(config_path="configs/provider_versions.json", registry_url="https://registry.terraform.io/")
    task_creator.create_tasks_json("tasks_.json")

