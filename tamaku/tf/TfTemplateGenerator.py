import os

from tamaku.utils.Utils import write_text_file


class TfTemplateGenerator:
    @staticmethod
    def generate_terraform_config(namespace: str, name: str, version: str, path: str):

        filename_with_path = os.path.join(path, "main.tf")
        template_str = """
terraform {
  required_providers {
    ${provider_name} = {
      source  = "${provider_namespace}/${provider_name}"
      version = "${provider_version}"
    }
  }
}
"""

        terraform_config = template_str.replace("${provider_name}", name)
        terraform_config = terraform_config.replace("${provider_namespace}", namespace)
        terraform_config = terraform_config.replace("${provider_version}", version)

        os.makedirs(path, exist_ok=True)

        write_text_file(filename_with_path, terraform_config)
