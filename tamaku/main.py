from tamaku.utils.Logger import Logger
from tamaku.tf.TfGetProviders import TfGetProviders
from tamaku.tf.TfInstalledVersionsChecker import TfInstalledVersionsChecker

logger = Logger()


def main():
    config_path = "configs/provider_config.json"
    # TfGetProviders(config_path)
    # logger.info("Terraform providers downloaded successfully")

    installed_providers = TfInstalledVersionsChecker(config_path)
    logger.info(f"Installed providers: {installed_providers.providers}")


if __name__ == "__main__":
    main()
