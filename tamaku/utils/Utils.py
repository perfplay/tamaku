import re

from tamaku.utils.Logger import Logger

logger = Logger()


def is_semantic_version(version):
    semantic_pattern = re.compile(r"^(v?\d+\.\d+\.\d+|v?\d+\.\d)$")
    return semantic_pattern.match(version) is not None
