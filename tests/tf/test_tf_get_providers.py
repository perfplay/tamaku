import unittest
from unittest.mock import patch, MagicMock

from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfRunProviderDownload import TfRunProviderDownload
from tamaku.tf.TfGetProviders import TfGetProviders
from tamaku.DataClasses import Config, Provider


class TestTfGetProviders(unittest.TestCase):

    @patch.object(TfProviderConfigLoader, 'load_config')
    @patch.object(TfTaskCreator, 'create_tasks_json')
    @patch.object(TfRunProviderDownload, 'run_download')
    @patch.object(Logger, 'info')
    def test_get_providers(self, mock_logger_info, mock_run_download, mock_create_tasks_json, mock_load_config):
        # Mocking the load_config to return a predefined config
        mock_load_config.return_value = Config(
            registry="registry.terraform.io",
            platforms=["linux_amd64", "darwin_arm64"],
            mirror_path="mirror",
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

        # Instantiate TfGetProviders to trigger the get_providers method
        TfGetProviders(config_path="configs/provider_config.json")

        # Assertions to ensure the methods were called with expected arguments
        expected_calls = [unittest.mock.call('configs/provider_config.json')]
        mock_load_config.assert_has_calls(expected_calls, any_order=False)
        mock_create_tasks_json.assert_called_once_with("provider_tasks.json")

        # Checking the calls for run_download
        expected_run_download_calls = [
            unittest.mock.call(namespace="hashicorp", name="aws", version="5.21.0", platform="linux_amd64",
                               path="mirror/providers"),
            unittest.mock.call(namespace="hashicorp", name="aws", version="5.21.0", platform="darwin_arm64",
                               path="mirror/providers"),
            unittest.mock.call(namespace="hashicorp", name="aws", version="5.35.0", platform="linux_amd64",
                               path="mirror/providers"),
            unittest.mock.call(namespace="hashicorp", name="aws", version="5.35.0", platform="darwin_arm64",
                               path="mirror/providers"),
            unittest.mock.call(namespace="hashicorp", name="helm", version="2.11.0", platform="linux_amd64",
                               path="mirror/providers"),
            unittest.mock.call(namespace="hashicorp", name="helm", version="2.11.0", platform="darwin_arm64",
                               path="mirror/providers")
        ]

        mock_run_download.assert_has_calls(expected_run_download_calls, any_order=True)
        self.assertEqual(mock_run_download.call_count, 6)
        mock_logger_info.assert_any_call("Terraform tasks created successfully")


if __name__ == '__main__':
    unittest.main()