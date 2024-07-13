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






