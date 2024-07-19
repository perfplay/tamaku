import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

from tamaku.tf.TfInstalledVersionsChecker import TfInstalledVersionsChecker
from tamaku.DataClasses import InstalledProvider, VersionWithPlatform, Config, Provider
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader


class TestTfInstalledVersionsChecker(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("builtins.open", new_callable=mock_open)
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
            ["aws"],  # Second call to listdir for provider names
            ["5.21.0.json", "5.35.0.json"]  # Third call to listdir for versions
        ]
        mock_isdir.return_value = True

        # Mocking the content of the version.json files
        def open_side_effect(path, *args, **kwargs):
            if "index.json" in path:
                return mock_open(read_data=json.dumps({
                    "versions": {
                        "5.21.0": {},
                        "5.35.0": {}
                    }
                })).return_value
            elif "5.21.0.json" in path:
                return mock_open(read_data=json.dumps({
                    "archives": {
                        "linux_amd64": {
                            "hashes": ["h1:N8sP6VZjHbtgmaCU6BKPox51UIypWXQRal7JMecEXQw="],
                            "url": "terraform-provider-aws_5.21.0_linux_amd64.zip"
                        },
                        "darwin_arm64": {
                            "hashes": ["h1:LzpydUV5m8hjktKbVyTPpRg8mjj67IXMKdOfanIfKNE="],
                            "url": "terraform-provider-aws_5.21.0_darwin_arm64.zip"
                        }
                    }
                })).return_value
            elif "5.35.0.json" in path:
                return mock_open(read_data=json.dumps({
                    "archives": {
                        "linux_amd64": {
                            "hashes": ["h1:N8sP6VZjHbtgmaCU6BKPox51UIypWXQRal7JMecEXQw="],
                            "url": "terraform-provider-aws_5.35.0_linux_amd64.zip"
                        },
                        "darwin_arm64": {
                            "hashes": ["h1:LzpydUV5m8hjktKbVyTPpRg8mjj67IXMKdOfanIfKNE="],
                            "url": "terraform-provider-aws_5.35.0_darwin_arm64.zip"
                        }
                    }
                })).return_value
            raise FileNotFoundError

        mock_open_file.side_effect = open_side_effect

        checker = TfInstalledVersionsChecker("dummy_path")

        expected_providers = [
            InstalledProvider(
                namespace="hashicorp",
                name="aws",
                versions=[
                    VersionWithPlatform(version="5.21.0", platform="linux_amd64"),
                    VersionWithPlatform(version="5.21.0", platform="darwin_arm64"),
                    VersionWithPlatform(version="5.35.0", platform="linux_amd64"),
                    VersionWithPlatform(version="5.35.0", platform="darwin_arm64")
                ]
            )
        ]

        self.assertEqual(checker.providers, expected_providers)
        mock_open_file.assert_any_call(
            os.path.join("mirror/v1/providers/registry.terraform.io/hashicorp/aws", "index.json"), 'r')


if __name__ == '__main__':
    unittest.main()
