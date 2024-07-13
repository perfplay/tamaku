import unittest
from unittest.mock import patch, mock_open
import json

from tamaku.BaseConfigLoader import BaseConfigLoader
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.DataClasses import Config, Provider


class TestBaseConfigLoader(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_config_file_success(self, mock_file):
        config = BaseConfigLoader.load_config_file("dummy_path")
        self.assertIsNotNone(config)
        self.assertEqual(config, {"key": "value"})

    @patch("builtins.open", side_effect=Exception("File not found"))
    def test_load_config_file_failure(self, mock_file):
        config = BaseConfigLoader.load_config_file("dummy_path")
        self.assertIsNone(config)


class TestTfProviderConfigLoader(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "registry": "registry.terraform.io",
        "platforms": ["linux_amd64", "darwin_arm64"],
        "mirror_path": None,
        "providers": [
            {
                "namespace": "hashicorp",
                "name": "aws",
                "minimal_version": None,
                "versions": []
            },
            {
                "namespace": "hashicorp",
                "name": "helm",
                "minimal_version": "2.13",
                "versions": []
            }
        ]
    }))
    def test_load_and_validate_config_success_empty_fields(self, mock_file):
        loader = TfProviderConfigLoader()
        config = loader.load_config("dummy_path")
        self.assertIsNotNone(config)
        self.assertIsInstance(config, Config)
        self.assertEqual(len(config.providers), 2)
        self.assertIsNone(config.providers[0].minimal_version)
        self.assertEqual(config.providers[0].versions, [])
        self.assertEqual(config.mirror_path, "mirror")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "registry": "registry.terraform.io",
        "platforms": ["linux_amd64", "darwin_arm64"],
        "mirror_path": "custom_mirror",
        "providers": [
            {
                "namespace": "hashicorp",
                "name": "aws",
                "minimal_version": "5.53",
                "versions": ["5.21.0", "5.35.0"]
            },
            {
                "namespace": "hashicorp",
                "name": "helm",
                "minimal_version": "2.13",
                "versions": ["2.11.0"]
            }
        ]
    }))
    def test_load_and_validate_config_success(self, mock_file):
        loader = TfProviderConfigLoader()
        config = loader.load_config("dummy_path")
        self.assertIsNotNone(config)
        self.assertIsInstance(config, Config)
        self.assertEqual(len(config.providers), 2)
        self.assertEqual(config.mirror_path, "custom_mirror")

    @patch("builtins.open", new_callable=mock_open, read_data='{"invalid_key": "value"}')
    def test_load_and_validate_config_failure(self, mock_file):
        loader = TfProviderConfigLoader()
        config = loader.load_config("dummy_path")
        self.assertIsNone(config)


if __name__ == '__main__':
    unittest.main()
