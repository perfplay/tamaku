from tamaku.utils.Logger import Logger
import subprocess
import threading

logger = Logger()


class CommandExecutor:
    def __init__(self):
        self.failed_updates = []

    def execute_command(self, command, timeout=300, **popen_kwargs):
        result = None
        try:
            result = self.run_subprocess_popen(command, timeout=timeout, **popen_kwargs)

            if result.returncode != 0:
                logger.error(f"Command failed with return code {result.returncode}")
                self.failed_updates.append((command, result.returncode))

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run command {command}: {e}")
            self.failed_updates.append((command, str(e)))
        except FileNotFoundError as e:
            logger.error(f"Command not found: {e}")
            self.failed_updates.append((command, str(e)))
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.failed_updates.append((command, str(e)))
        return result

    def run_subprocess_popen(self, command, timeout=300, **popen_kwargs):
        default_popen_kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True,
            'bufsize': 1,
            'universal_newlines': True
        }

        final_popen_kwargs = {**default_popen_kwargs, **popen_kwargs}

        process = subprocess.Popen(command, **final_popen_kwargs)

        stdout_thread = threading.Thread(target=self.read_stream, args=(process.stdout, "STDOUT"))
        stderr_thread = threading.Thread(target=self.read_stream, args=(process.stderr, "STDERR"))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            logger.debug(f"stdout: {stdout}")
            logger.debug(f"stderr: {stderr}")
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            logger.error(f"Process timed out: {stderr}")
        except Exception as e:
            logger.error(f"Error during communicate: {e}")
            stdout, stderr = "", ""

        if stdout is None:
            stdout = ""
        if stderr is None:
            stderr = ""

        process.wait()
        return process

    @staticmethod
    def read_stream(stream, stream_name):
        try:
            for line in iter(stream.readline, ''):
                if line:
                    if stream_name == "STDERR":
                        logger.error(f"{stream_name}: {line.strip()}")
                    else:
                        logger.info(f"{stream_name}: {line.strip()}")
        except ValueError as e:
            logger.error(f"Error reading stream: {e}")
        finally:
            stream.close()
