import unittest
import tempfile
import json
from unittest.mock import patch, MagicMock
from tamaku.tf.TfTaskCreator import TfTaskCreator
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfProviderVersionFetcher import TfProviderVersionFetcher
from tamaku.utils.Logger import Logger

logger = Logger()


class TestTfTaskCreator(unittest.TestCase):

    @patch.object(TfProviderConfigLoader, 'load_config')
    @patch.object(TfProviderVersionFetcher, 'fetch_versions')
    def test_create_tasks(self, mock_fetch_versions, mock_load_config):
        mock_load_config.return_value = {
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
        }

        mock_fetch_versions.side_effect = [
            ["5.11.0", "5.21.0", "5.35.0", "5.53.0", "5.54.0"],
            ["2.10.0", "2.11.0", "2.13.0"]
        ]

        task_creator = TfTaskCreator("path/to/config.json", "https://registry.url")
        tasks = task_creator.create_tasks()

        expected_tasks = {
            "tasks": [
                {
                    "namespace": "hashicorp",
                    "name": "aws",
                    "versions": ["5.21.0", "5.35.0", "5.53.0", "5.54.0"]
                },
                {
                    "namespace": "hashicorp",
                    "name": "helm",
                    "versions": ["2.11.0", "2.13.0"]
                }
            ]
        }

        self.assertEqual(tasks, expected_tasks)

    @patch.object(TfProviderVersionFetcher, 'fetch_versions')
    @patch.object(TfProviderConfigLoader, 'load_config')
    def test_create_tasks_json(self, mock_load_config, mock_fetch_versions):
        mock_load_config.return_value = {
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
        }

        mock_fetch_versions.side_effect = [
            ["5.11.0", "5.21.0", "5.35.0", "5.53.0", "5.54.0"],
            ["2.10.0", "2.11.0", "2.13.0"]
        ]

        task_creator = TfTaskCreator("path/to/config.json", "https://registry.url")

        with self.assertLogs(logger.logger, level='INFO') as log:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                filename = temp_file.name

            task_creator.create_tasks_json(filename)

            with open(filename, 'r') as file:
                data = json.load(file)

            expected_tasks = {
                "tasks": [
                    {
                        "namespace": "hashicorp",
                        "name": "aws",
                        "versions": ["5.21.0", "5.35.0", "5.53.0", "5.54.0"]
                    },
                    {
                        "namespace": "hashicorp",
                        "name": "helm",
                        "versions": ["2.11.0", "2.13.0"]
                    }
                ]
            }

            self.assertEqual(data, expected_tasks)
            self.assertIn(f"INFO:tamaku.utils.Logger:Generated JSON file: {filename}", log.output)


if __name__ == '__main__':
    unittest.main()
