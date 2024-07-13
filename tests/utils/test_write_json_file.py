import unittest
from unittest.mock import mock_open, patch
import json
from tamaku.utils.Utils import write_json_file
from tamaku.utils.Logger import Logger

logger = Logger()


class TestWriteJsonFile(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(logger.logger, 'info')
    def test_write_json_file_success(self, mock_logger_info, mock_file):
        data = {"key": "value"}
        filename = "dummy_path.json"

        write_json_file(filename, data)

        mock_file.assert_called_once_with(filename, 'w')
        handle = mock_file()
        handle.write.assert_called()
        written_data = ''.join(call.args[0] for call in handle.write.mock_calls)
        expected_data = json.dumps(data, indent=4)
        self.assertEqual(written_data, expected_data)
        mock_logger_info.assert_called_once_with(f"Generated JSON file: {filename}")

    @patch("builtins.open", new_callable=mock_open)
    @patch.object(logger.logger, 'error')
    def test_write_json_file_ioerror(self, mock_logger_error, mock_file):
        data = {"key": "value"}
        filename = "dummy_path.json"

        mock_file.side_effect = IOError("File write error")

        write_json_file(filename, data)

        mock_file.assert_called_once_with(filename, 'w')
        mock_logger_error.assert_called_once_with(f"Failed to write JSON file: File write error")


if __name__ == '__main__':
    unittest.main()
