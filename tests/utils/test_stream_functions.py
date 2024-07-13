import unittest
from unittest.mock import patch, MagicMock
import subprocess
import threading
from tamaku.utils.Logger import Logger
from tamaku.utils.CommandExecutor import CommandExecutor

logging = Logger()


class TestStreamFunctions(unittest.TestCase):

    @patch.object(logging.logger, 'info')
    def test_read_stream_stdout(self, mock_logger_info):
        mock_stream = MagicMock()
        mock_stream.readline.side_effect = ["line1\n", "line2\n", ""]

        CommandExecutor.read_stream(mock_stream, "STDOUT")

        expected_calls = [
            unittest.mock.call("STDOUT: line1"),
            unittest.mock.call("STDOUT: line2"),
        ]
        mock_logger_info.assert_has_calls(expected_calls, any_order=False)

    @patch.object(logging.logger, 'error')
    def test_read_stream_stderr(self, mock_logger_error):
        mock_stream = MagicMock()
        mock_stream.readline.side_effect = ["error1\n", "error2\n", ""]

        CommandExecutor.read_stream(mock_stream, "STDERR")

        expected_calls = [
            unittest.mock.call("STDERR: error1"),
            unittest.mock.call("STDERR: error2"),
        ]
        mock_logger_error.assert_has_calls(expected_calls, any_order=False)

    @patch('subprocess.Popen')
    @patch('threading.Thread')
    def test_run_subprocess_popen(self, mock_thread, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = MagicMock()
        mock_process.stderr = MagicMock()
        mock_process.communicate.return_value = ("stdout", "stderr")
        mock_popen.return_value = mock_process

        command_exe = CommandExecutor()
        result = command_exe.run_subprocess_popen(['echo', 'test'])

        mock_popen.assert_called_once_with(
            ['echo', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, universal_newlines=True
        )

        self.assertEqual(result, mock_process)

    @patch('subprocess.Popen')
    @patch('threading.Thread')
    @patch.object(logging.logger, 'error')
    def test_execute_command(self, mock_logger_error, mock_thread, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = MagicMock()
        mock_process.stderr = MagicMock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = ("stdout", "stderr")
        mock_popen.return_value = mock_process

        command_exe = CommandExecutor()
        command_exe.execute_command(['echo', 'test'])

        mock_popen.assert_called_once_with(
            ['echo', 'test'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, universal_newlines=True
        )
        mock_logger_error.assert_any_call("Command failed with return code 1")
        self.assertEqual(len(command_exe.failed_updates), 1)


if __name__ == '__main__':
    unittest.main()
