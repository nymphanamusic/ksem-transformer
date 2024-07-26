from typing import cast

from hypothesis import assume, example, given
from hypothesis import strategies as st

from ksem_transformer.utils.tree import deep_join_trees

AnyScalar = st.deferred(
    lambda: (st.none() | st.booleans() | st.integers() | st.floats() | st.text())
)
AnyList = st.deferred(lambda: st.lists(AnyObject))
AnyDict = st.deferred(lambda: st.dictionaries(AnyScalar, AnyObject))
AnyObject = st.deferred(lambda: (AnyScalar | AnyList | AnyDict))

config_example = {
    "root": {
        "vsl": {
            "settings": {"middle_c": "C5"},
            "strings": {
                "violin": {"velocities": [-1, -2]},
                "cello": {"note": "A8", "velocities": [7, 8]},
            },
        },
        "bbc": {
            "strings": {
                "violin": {"note": "F1", "velocities": [10, 11]},
                "cello": {"note": "G1", "velocities": [12, 13]},
            },
            "woodwinds": {"oboe": {"note": "A1", "velocities": [14, 15]}},
        },
    }
}


# This function is only used for property testing, which is kind of dumb because
# I'm only expanding my surface area for errors, but I wrote tests for this that
# I feel confident close the testability loop
def get_node_paths(
    obj: object, _parent_path: tuple[object, ...] | None = None
) -> list[tuple[object, ...]]:
    if _parent_path is None:
        _parent_path = ()

    if not isinstance(obj, dict):
        return [_parent_path] if _parent_path else []

    return ([_parent_path] if _parent_path else []) + [
        node
        for k, v in cast(dict[object, object], obj).items()
        for node in get_node_paths(v, _parent_path + (k,))
    ]


class TestGetKeyPaths:
    @given(AnyObject)
    def test_returns_empty_list_if_not_dict(self, obj: object):
        assume(not isinstance(obj, dict))
        assert get_node_paths(obj) == []

    @given(AnyDict)
    def test_returns_populated_list_if_dict(self, obj: dict[object, object]):
        assume(len(obj) > 0)

        keys = get_node_paths(obj)
        assert isinstance(keys, list)
        assert len(keys) > 0

    @given(AnyObject)
    def test_does_not_return_empty_tuple(self, obj: object):
        assert () not in get_node_paths(obj)

    @given(AnyObject)
    def test_returns_list_of_tuples(self, obj: object):
        keys = get_node_paths(obj)
        assert isinstance(keys, list)
        assert all(isinstance(i, tuple) for i in keys)

    @given(AnyObject)
    def test_no_duplicates(self, obj: object):
        keys = get_node_paths(obj)
        assert len(set(keys)) == len(keys)

    @given(AnyDict)
    @example(config_example)
    def test_every_key_was_found(self, obj: dict[object, object]):
        """Test that every key in the tree was found.

        This test works by iterating depth-first (moving from leaf nodes up to the
        root) through the list of all key paths in the tree. We remove each node from
        the tree as we're iterating, and at the end, we check that we're left with an
        empty tree.

        This works because if we try to delete a node that's already been deleted, an
        error is raised, and we expect `get_key_paths` to give us a path to every node.
        """

        # Iterate depth-first
        for node_path in sorted(
            get_node_paths(obj), key=lambda x: len(x), reverse=True
        ):
            # Get the parent of the leaf node represented by this key tuple
            parent: object = None
            child: object = obj

            for key in node_path:
                parent = child
                assert isinstance(parent, dict)
                child: object = cast(dict[object, object], parent)[key]

            assert not isinstance(child, dict) or child == {}
            if parent is not None:
                # Delete the leaf node from its parent
                del parent[node_path[-1]]
        assert obj == {}


class TestDeepJoinTrees:
    def test_overwrite_existing(self):
        assert deep_join_trees({"a": 1}, {"a": 2}) == {"a": 2}

    def test_add_when_not_existing(self):
        actual = deep_join_trees({"a": 1}, {"b": 2})
        expected = {"a": 1, "b": 2}
        assert actual == expected

    def test_deep(self):
        assert deep_join_trees({"a": {"b": 1}}, {"a": {"b": 2, "c": 2}}) == {
            "a": {"b": 2, "c": 2}
        }

    @given(AnyDict, AnyDict)
    def test_does_not_raise(
        self, tree1: dict[object, object], tree2: dict[object, object]
    ):
        deep_join_trees(tree1, tree2)

    @given(AnyDict, AnyDict)
    def test_no_keys_lost(
        self, tree1: dict[object, object], tree2: dict[object, object]
    ):
        # This is a very poor assumption, but I don't know how to write a more
        # precise generator without losing my mind
        assume(not set(get_node_paths(tree1)) & set(get_node_paths(tree2)))
        joined = deep_join_trees(tree2, tree1)
        assert set(get_node_paths(tree1)) | set(get_node_paths(tree2)) == set(
            get_node_paths(joined)
        )
