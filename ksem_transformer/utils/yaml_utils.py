# pyright: reportUnknownMemberType=none, reportUnknownVariableType=none

from io import StringIO
from typing import Any

import ruamel.yaml  # pyright: ignore[reportMissingTypeStubs]
import ruamel.yaml.comments

yaml = ruamel.yaml.YAML(typ="rt")


def yaml_load(data: Any) -> ruamel.yaml.comments.CommentedMap:
    stream = StringIO()
    yaml.dump(data, stream)
    stream.seek(0)
    return yaml.load(stream)


def yaml_dumps(yaml_data: ruamel.yaml.comments.CommentedMap) -> str:
    stream = StringIO()
    yaml.dump(yaml_data, stream)
    return stream.getvalue()
