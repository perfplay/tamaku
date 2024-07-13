import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

from tamaku.tf.TfInstalledVersionsChecker import TfInstalledVersionsChecker
from tamaku.DataClasses import InstalledProvider, Config, Provider
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader


class TestTfInstalledVersionsChecker(unittest.TestCase):

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "versions": {
            "5.21.0": {},
            "5.35.0": {}
        }
    }))
    @patch.object(TfProviderConfigLoader, 'load_config')
    def test_check_installed_versions(self, mock_load_config, mock_open_file, mock_isdir, mock_listdir):
        # Mocking the config to be loaded
        mock_load_config.return_value = Config(
            registry="registry.terraform.io",
            mirror_path="mirror",
            platforms=["linux_amd64", "darwin_arm64"],
            providers=[
                Provider(
                    namespace="hashicorp",
                    name="aws",
                    minimal_version="5.53",
                    versions=["5.21.0", "5.35.0"]
                )
            ]
        )

        # Mocking os.listdir and os.path.isdir
        mock_listdir.side_effect = [
            ["hashicorp"],  # First call to listdir for namespaces
            ["aws"],       # Second call to listdir for provider names
        ]
        mock_isdir.return_value = True

        checker = TfInstalledVersionsChecker("dummy_path")

        expected_providers = [
            InstalledProvider(
                namespace="hashicorp",
                name="aws",
                versions=["5.21.0", "5.35.0"]
            )
        ]

        self.assertEqual(checker.providers, expected_providers)
        mock_open_file.assert_called_with(os.path.join("mirror/providers/registry.terraform.io/hashicorp/aws", "index.json"), 'r')

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("builtins.open")
    @patch.object(TfProviderConfigLoader, 'load_config')
    def test_check_installed_versions_multiple_providers(self, mock_load_config, mock_open_file, mock_isdir, mock_listdir):
        # Mocking the config to be loaded
        mock_load_config.return_value = Config(
            registry="registry.terraform.io",
            mirror_path="mirror",
            platforms=["linux_amd64", "darwin_arm64"],
            providers=[
                Provider(
                    namespace="hashicorp",
                    name="aws",
                    minimal_version="5.53",
                    versions=["5.21.0", "5.35.0"]
                ),
                Provider(
                    namespace="hashicorp",
                    name="helm",
                    minimal_version="2.13",
                    versions=["2.11.0"]
                )
            ]
        )

        # Mocking os.listdir and os.path.isdir
        mock_listdir.side_effect = [
            ["hashicorp"],  # First call to listdir for namespaces
            ["aws", "helm"],  # Second call to listdir for provider names
            ["5.21.0.json", "5.35.0.json"],  # Third call for aws versions
            ["2.11.0.json", "2.13.0.json"],  # Fourth call for helm versions
        ]
        mock_isdir.return_value = True

        # Mocking the content of the index.json for each provider
        def open_side_effect(path, *args, **kwargs):
            if "aws" in path:
                return mock_open(read_data=json.dumps({
                    "versions": {
                        "5.21.0": {},
                        "5.35.0": {}
                    }
                })).return_value
            elif "helm" in path:
                return mock_open(read_data=json.dumps({
                    "versions": {
                        "2.11.0": {},
                        "2.13.0": {}
                    }
                })).return_value
            raise FileNotFoundError

        mock_open_file.side_effect = open_side_effect

        checker = TfInstalledVersionsChecker("dummy_path")

        expected_providers = [
            InstalledProvider(
                namespace="hashicorp",
                name="aws",
                versions=["5.21.0", "5.35.0"]
            ),
            InstalledProvider(
                namespace="hashicorp",
                name="helm",
                versions=["2.11.0", "2.13.0"]
            )
        ]

        self.assertEqual(checker.providers, expected_providers)
        mock_open_file.assert_any_call(os.path.join("mirror/providers/registry.terraform.io/hashicorp/aws", "index.json"), 'r')
        mock_open_file.assert_any_call(os.path.join("mirror/providers/registry.terraform.io/hashicorp/helm", "index.json"), 'r')


if __name__ == '__main__':
    unittest.main()
