import os
from tamaku.utils.CommandExecutor import CommandExecutor
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator
from tamaku.utils.Logger import Logger

logger = Logger()


class TfRunProviderDownload:
    def __init__(self):
        self.failed_updates = []

    def run_download(self, namespace: str, name: str, version: str, platform: str, path: str):
        logger.info(f"Starting download for {namespace}/{name} version {version} on {platform}")
        TfTemplateGenerator.generate_terraform_config(namespace, name, version, path)
        command = ["terraform", "providers", "mirror", f"-platform={platform}", "."]

        logger.info(f"Downloading {namespace}/{name} version {version} for {platform}...")
        logger.info(f"Running command: {' '.join(command)}")

        original_cwd = os.getcwd()

        try:
            os.chdir(path)

            exe = CommandExecutor()
            result = exe.execute_command(command)
            if result and result.returncode == 0:
                logger.info(f"Downloaded {namespace}/{name} version {version} for {platform} successfully")
            else:
                logger.error(f"Failed to download {namespace}/{name} version {version} for {platform}")
                self.failed_updates.append(f"{namespace}/{name} version {version} for {platform}")
        finally:
            os.chdir(original_cwd)
