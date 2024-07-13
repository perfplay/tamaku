from tamaku.DataClasses import Provider
from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfRunProviderDownload import TfRunProviderDownload

logger = Logger()


class TfGetProviders:
    def __init__(self, config_path: str):
        self.get_providers(config_path)

    @staticmethod
    def get_providers(config_path: str = None):
        loader = TfProviderConfigLoader()
        config = loader.load_config(config_path)

        task_creator = TfTaskCreator(config_path=config_path, registry_url=config.registry)
        task_creator.create_tasks_json("provider_tasks.json")
        logger.info("Terraform tasks created successfully")

        mirror_path = f"{config.mirror_path}/providers"

        for platform in config.platforms:
            for provider_data in task_creator.tasks["providers"]:
                provider = Provider.from_dict(provider_data)
                logger.info(f"Processing provider {provider.namespace}/{provider.name} with versions {provider.versions}")
                for version in provider.versions:
                    tf_run_provider_download = TfRunProviderDownload()
                    tf_run_provider_download.run_download(namespace=provider.namespace,
                                                          name=provider.name, version=version,
                                                          platform=platform, path=mirror_path)