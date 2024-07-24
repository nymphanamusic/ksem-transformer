from __future__ import annotations

from collections.abc import MutableMapping
from copy import deepcopy
from typing import cast

type Tree = MutableMapping[object, object]


def deep_join_trees(tree1: Tree, tree2: Tree) -> Tree:
    out = deepcopy(tree1)

    for k, v in tree2.items():
        if (
            isinstance(v, MutableMapping)
            and k in out
            and isinstance(out[k], MutableMapping)
        ):
            # Merge this mapping into the one in out
            out[k] = deep_join_trees(cast(Tree, out[k]), cast(Tree, v))
        else:
            out[k] = v

    return out
