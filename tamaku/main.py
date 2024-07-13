from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator

logger = Logger()


def main():
    config_path = "configs/provider_config.json"
    task_creator = TfTaskCreator(config_path=config_path, registry_url="https://registry.terraform.io/")
    task_creator.create_tasks_json("tasks_.json")
    logger.info("Terraform tasks created successfully")

    tf_template_generator = TfTemplateGenerator()
    tf_template_generator.generate_terraform_config(namespace="hashicorp", name="aws", version="3.0.0", path="mirror/providers")
