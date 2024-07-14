import unittest
from unittest.mock import patch, MagicMock

from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfRunProviderDownload import TfRunProviderDownload
from tamaku.tf.TfGetProviders import TfGetProviders
from tamaku.DataClasses import Config, Provider, VersionWithPlatform

logger = Logger()

class TestTfGetProviders(unittest.TestCase):

    @patch.object(TfProviderConfigLoader, 'load_config')
    @patch.object(TfTaskCreator, 'create_tasks_json')
    @patch.object(TfRunProviderDownload, 'run_download')
    @patch.object(Logger, 'info')
    @patch('requests.get')
    def test_get_providers(self, mock_requests_get, mock_logger_info, mock_run_download, mock_create_tasks_json, mock_load_config):
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
                    versions=[
                        "5.21.0",
                        "5.21.0",
                        "5.35.0",
                        "5.35.0",
                    ]
                ),
                Provider(
                    namespace="hashicorp",
                    name="helm",
                    minimal_version="2.13",
                    versions=[
                        "2.11.0",
                        "2.11.0",
                    ]
                )
            ]
        )

        def mock_fetch_versions(url, *args, **kwargs):
            if "aws" in url:
                return MagicMock(status_code=200, json=lambda: {"versions": [{"version": "5.21.0"}, {"version": "5.35.0"}]})
            elif "helm" in url:
                return MagicMock(status_code=200, json=lambda: {"versions": [{"version": "2.11.0"}]})
            return MagicMock(status_code=200, json=lambda: {"versions": []})

        mock_requests_get.side_effect = mock_fetch_versions

        mock_create_tasks_json.return_value = None
        mock_task_creator = MagicMock()
        mock_task_creator.tasks = {
            "providers": [
                {
                    "namespace": "hashicorp",
                    "name": "aws",
                    "versions": [
                        {"version": "5.21.0", "platform": "linux_amd64"},
                        {"version": "5.21.0", "platform": "darwin_arm64"},
                        {"version": "5.35.0", "platform": "linux_amd64"},
                        {"version": "5.35.0", "platform": "darwin_arm64"}
                    ]
                },
                {
                    "namespace": "hashicorp",
                    "name": "helm",
                    "versions": [
                        {"version": "2.11.0", "platform": "linux_amd64"},
                        {"version": "2.11.0", "platform": "darwin_arm64"}
                    ]
                }
            ]
        }

        with patch('tamaku.tf.TfTaskCreator.TfTaskCreator', return_value=mock_task_creator):
            TfGetProviders(config_path="configs/provider_config.json")

        expected_calls = [unittest.mock.call("configs/provider_config.json")]
        mock_load_config.assert_has_calls(expected_calls, any_order=False)
        mock_create_tasks_json.assert_called_once_with("provider_tasks.json")

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