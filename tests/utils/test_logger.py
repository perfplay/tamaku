import unittest
from unittest.mock import patch
from io import StringIO
from tamaku.utils.Logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.stdout_output = StringIO()
        self.stderr_output = StringIO()
        self.stdout_patcher = patch('sys.stdout', new=self.stdout_output)
        self.stderr_patcher = patch('sys.stderr', new=self.stderr_output)
        self.stdout_patcher.start()
        self.stderr_patcher.start()
        self.logger = Logger(log_level='DEBUG')

    def tearDown(self):
        self.stdout_patcher.stop()
        self.stderr_patcher.stop()

    def test_debug_message(self):
        self.logger.debug('This is a debug message')
        self.assertIn('DEBUG', self.stdout_output.getvalue())
        self.assertIn('This is a debug message', self.stdout_output.getvalue())

    def test_info_message(self):
        self.logger.info('This is an info message')
        self.assertIn('INFO', self.stdout_output.getvalue())
        self.assertIn('This is an info message', self.stdout_output.getvalue())

    def test_warning_message(self):
        self.logger.warning('This is a warning message')
        self.assertIn('WARNING', self.stderr_output.getvalue())
        self.assertIn('This is a warning message', self.stderr_output.getvalue())

    def test_error_message(self):
        self.logger.error('This is an error message')
        self.assertIn('ERROR', self.stderr_output.getvalue())
        self.assertIn('This is an error message', self.stderr_output.getvalue())

    def test_critical_message(self):
        self.logger.critical('This is a critical message')
        self.assertIn('CRITICAL', self.stderr_output.getvalue())
        self.assertIn('This is a critical message', self.stderr_output.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_error_message_to_stderr(self, mock_stderr):
        logger = Logger(log_level='DEBUG')
        logger.error('This is an error message')
        self.assertIn('ERROR', mock_stderr.getvalue())
        self.assertIn('This is an error message', mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_critical_message_to_stderr(self, mock_stderr):
        logger = Logger(log_level='DEBUG')
        logger.critical('This is a critical message')
        self.assertIn('CRITICAL', mock_stderr.getvalue())
        self.assertIn('This is a critical message', mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
