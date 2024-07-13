import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
from tamaku.tf.TfRunProviderDownload import TfRunProviderDownload
from tamaku.utils.Logger import Logger

logger = Logger()


class TestTfRunProviderDownload(unittest.TestCase):

    @patch.object(Logger, 'info')
    @patch.object(Logger, 'error')
    def test_run_download(self, mock_logger_info, mock_logger_error):
        temp_dir = tempfile.mkdtemp()

        try:
            namespace = "hashicorp"
            name = "aws"
            version = "5.55.0"
            platform = "darwin_arm64"
            path = os.path.join(temp_dir, "mirror", "providers")

            downloader = TfRunProviderDownload()
            downloader.run_download(namespace, name, version, platform, path)

            expected_files = [
                os.path.join(path, "registry.terraform.io", "hashicorp", "aws", "5.55.0.json"),
                os.path.join(path, "registry.terraform.io", "hashicorp", "aws", "index.json"),
                os.path.join(path, "registry.terraform.io", "hashicorp", "aws",
                             "terraform-provider-aws_5.55.0_darwin_arm64.zip")
            ]

            for file_path in expected_files:
                self.assertTrue(os.path.isfile(file_path), f"File {file_path} not found")

        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()