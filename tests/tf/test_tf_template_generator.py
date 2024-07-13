import unittest
import tempfile
import os
from tamaku.tf.TfTemplateGenerator import TfTemplateGenerator


class TestTfTemplateGenerator(unittest.TestCase):

    def test_generate_terraform_config(self):
        namespace = "hashicorp"
        name = "aws"
        version = "3.27.0"

        expected_config = """
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.27.0"
    }
  }
}
        """.strip()

        with tempfile.TemporaryDirectory() as temp_dir:
            TfTemplateGenerator.generate_terraform_config(namespace, name, version, temp_dir)
            generated_file_path = os.path.join(temp_dir, "main.tf")

            with open(generated_file_path, 'r') as file:
                generated_config = file.read().strip()

            self.assertEqual(generated_config, expected_config)


if __name__ == '__main__':
    unittest.main()