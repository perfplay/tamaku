import unittest
from unittest.mock import patch, MagicMock
import requests
from packaging import version

from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderVersionFetcher import TfProviderVersionFetcher

logger = Logger()


class TestTfProviderVersionFetcher(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_versions(self, mock_get):
        # Mocking the JSON response from the API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "versions": [
                {"version": "3.0"},
                {"version": "1.0.0"},
                {"version": "2.0.0-alpha"},  # Non-semantic version
                {"version": "invalid_version"},  # Invalid version
                {"version": "2.0.0"}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        fetcher = TfProviderVersionFetcher("https://example.com", "namespace", "name")
        fetcher.fetch_versions()

        expected_versions = [version.parse("1.0.0"), version.parse("2.0.0"), version.parse("3.0")]
        expected_versions_str = ["1.0.0", "2.0.0", "3.0"]

        self.assertEqual(fetcher.current_versions, expected_versions)
        self.assertEqual(fetcher.current_versions_str, expected_versions_str)

        with self.assertLogs(logger.logger_name, level='WARNING') as log:
            fetcher.fetch_versions()
            self.assertIn(f"WARNING:{logger.logger_name}:Non-semantic version, filtered: 2.0.0-alpha", log.output)
            self.assertIn(f"WARNING:{logger.logger_name}:Invalid version: invalid_version - Invalid version: 'invalid_version'", log.output)

    @patch('requests.get')
    def test_fetch_versions_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("API error")

        fetcher = TfProviderVersionFetcher("https://example.com", "namespace", "name")

        with self.assertLogs('tamaku.utils.Logger', level='ERROR') as log:
            fetcher.fetch_versions()
            self.assertIn(f"ERROR:{logger.logger_name}:Failed to fetch versions for namespace/name: API error", log.output)


if __name__ == '__main__':
    unittest.main()
