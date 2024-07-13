from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator
from tamaku.tf.TfRunProviderDownload import TfRunProviderDownload

logger = Logger()


def main():
    config_path = "configs/provider_config.json"
    task_creator = TfTaskCreator(config_path=config_path, registry_url="https://registry.terraform.io/")
    task_creator.create_tasks_json("tasks_.json")
    logger.info("Terraform tasks created successfully")

    tf_template_generator = TfTemplateGenerator()
    tf_template_generator.generate_terraform_config(namespace="hashicorp",
                                                    name="aws",
                                                    version="5.55.0", path="mirror/providers")

    tf_run_provider_download = TfRunProviderDownload()
    tf_run_provider_download.run_download(namespace="hashicorp",
                                          name="aws", version="5.55.0",
                                          platform="darwin_arm64", path="mirror/providers")


if __name__ == "__main__":
    main()
