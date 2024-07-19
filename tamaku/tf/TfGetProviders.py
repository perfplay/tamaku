from tamaku.DataClasses import TaskProvider, VersionWithPlatform
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator
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

        mirror_path = f"{config.mirror_path}/v1/providers"

        for provider_data in task_creator.tasks["providers"]:
            task_provider = TaskProvider.from_dict(provider_data)
            logger.info(f"Processing provider {task_provider.namespace}/{task_provider.name} with versions {task_provider.versions}")
            for version_with_platform in task_provider.versions:
                tf_run_provider_download = TfRunProviderDownload()
                logger.debug(f"Downloading {task_provider.namespace}/{task_provider.name} version {version_with_platform.version} for {version_with_platform.platform}")
                tf_run_provider_download.run_download(namespace=task_provider.namespace,
                                                      name=task_provider.name, version=version_with_platform.version,
                                                      platform=version_with_platform.platform, path=mirror_path)
        TfTemplateGenerator.generate_mirror_well_known_file(config.mirror_path)

