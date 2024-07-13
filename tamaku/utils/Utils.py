import json
import re
import subprocess
import threading
from typing import Dict, Any

from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.utils.Logger import Logger

logger = Logger()


def is_semantic_version(version):
    semantic_pattern = re.compile(r"^(v?\d+\.\d+\.\d+|v?\d+\.\d)$")
    return semantic_pattern.match(version) is not None


def write_json_file(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Generated JSON file: {filename}")
    except IOError as e:
        logger.error(f"Failed to write JSON file: {e}")


def write_text_file(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write(data)
        logger.info(f"Generated file: {filename}")
    except IOError as e:
        logger.error(f"Failed to write file: {e}")


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


def run_subprocess_popen(command, timeout=300):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1,
                               universal_newlines=True)

    stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, "STDOUT"))
    stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, "STDERR"))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        logger.error(f"Process timed out: {stderr}")

    process.wait()
    return process
