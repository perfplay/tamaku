import unittest
from tamaku.utils.Utils import is_semantic_version


class TestSemanticVersion(unittest.TestCase):
    def test_valid_versions(self):
        valid_versions = [
            "0.1",
            "1.0",
            "1.0.0",
            "0.1.0",
            "0.0.1",
            "10.20.30",
            "v1.2",
            "v1.2.3",
            "v0.0.1"
        ]
        for version in valid_versions:
            with self.subTest(version=version):
                self.assertTrue(is_semantic_version(version), f"Failed for version: {version}")

    def test_invalid_versions(self):
        invalid_versions = [
            "1",
            "v1",
            "1.0.0.0",
            "v1.2.3.4",
            "a.b.c",
            "1.0.0-alpha",
            "1.0.0+build",
            "1.0.0-alpha+build"
        ]
        for version in invalid_versions:
            with self.subTest(version=version):
                self.assertFalse(is_semantic_version(version), f"Failed for version: {version}")


if __name__ == '__main__':
    unittest.main()
