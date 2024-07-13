import subprocess
from tamaku.utils.Utils import run_subprocess_popen
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator
from tamaku.utils.Logger import Logger

logger = Logger()


class TfRunProviderDownload:
    def __init__(self):
        self.failed_updates = []

    def run_download(self, namespace: str, name: str, version: str,
                     platform: str, path: str):

        TfTemplateGenerator.generate_terraform_config(namespace, name, version, path)
        command = ["terraform", "mirror", f"-platform={platform}", path]

        self._execute_command(command)

