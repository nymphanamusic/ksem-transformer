from __future__ import annotations

from collections.abc import MutableMapping
from copy import deepcopy
from typing import Any, cast

type Tree[K, V] = MutableMapping[K, V]


def deep_join_trees[K, V](tree1: Tree[K, V], tree2: Tree[K, V]) -> Tree[K, V]:
    out = deepcopy(tree1)

    for k, v in tree2.items():
        if (
            isinstance(v, MutableMapping)
            and k in out
            and isinstance(out[k], MutableMapping)
        ):
            # Merge this mapping into the one in out
            out[k] = cast(
                Any,  # Sorry, taking the cheater's route here :(
                deep_join_trees(
                    cast(Tree[object, object], out[k]), cast(Tree[object, object], v)
                ),
            )
        else:
            out[k] = v

    return out
