from tamaku.utils.VersionFilter import VersionFilter
import unittest
from tamaku.utils.Logger import Logger

logger = Logger()


class TestVersionFilter(unittest.TestCase):

    def test_filter_versions(self):
        versions = ["1.0.0", "2.0.0-alpha", "1.0.1", "2.0.0", "0.9.0"]
        exclude = ["2.0.0-alpha"]
        include = ["1.0.1"]
        min_version = "1.0.0"

        version_filter = VersionFilter(versions, exclude, include, min_version)
        filtered_versions = version_filter.filter_versions()
        expected_versions = ["1.0.0", "1.0.1", "2.0.0"]

        self.assertEqual(filtered_versions, expected_versions)

    def test_no_exclusions(self):
        versions = ["1.0.0", "2.0.0", "1.0.1"]
        version_filter = VersionFilter(versions)
        filtered_versions = version_filter.filter_versions()
        expected_versions = ["1.0.0", "1.0.1", "2.0.0"]

        self.assertEqual(filtered_versions, expected_versions)

    def test_with_min_version(self):
        versions = ["1.0.0", "0.9.0", "1.1.0"]
        min_version = "1.0.0"
        version_filter = VersionFilter(versions, min_version=min_version)
        filtered_versions = version_filter.filter_versions()
        expected_versions = ["1.0.0", "1.1.0"]

        self.assertEqual(filtered_versions, expected_versions)

    def test_include_versions(self):
        versions = ["1.0.0", "1.1.0"]
        include = ["1.2.0"]
        version_filter = VersionFilter(versions, include=include)
        filtered_versions = version_filter.filter_versions()
        expected_versions = ["1.0.0", "1.1.0"]

        self.assertEqual(filtered_versions, expected_versions)

    def test_include_with_warning(self):
        versions = ["1.0.0", "1.1.0", "1.2.0", "1.3.0"]
        include = ["1.5.0", "1.0.0"]
        min_version = "1.2.0"
        version_filter = VersionFilter(versions, include=include, min_version=min_version)
        with self.assertLogs(logger.logger_name, level='WARNING') as log:
            filtered_versions = version_filter.filter_versions()
            self.assertIn(f"WARNING:{logger.logger_name}:Included version not found in original list: 1.5.0", log.output)
        expected_versions = ["1.0.0", "1.2.0", "1.3.0"]

        self.assertEqual(filtered_versions, expected_versions)

    def test_exclude_versions(self):
        versions = ["1.0.0", "1.1.0", "1.2.0"]
        exclude = ["1.1.0"]
        version_filter = VersionFilter(versions, exclude=exclude)
        filtered_versions = version_filter.filter_versions()
        expected_versions = ["1.0.0", "1.2.0"]

        self.assertEqual(filtered_versions, expected_versions)


if __name__ == '__main__':
    unittest.main()
