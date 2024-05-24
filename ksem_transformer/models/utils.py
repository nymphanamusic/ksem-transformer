def combine_dicts[K, V](*dicts: dict[K, V]) -> dict[K, V]:
    """
    Combines multiple dictionaries into one, prioritizing non-None values.
    """
    out: dict[K, V] = {}
    for dict_ in dicts:
        for k, v in dict_.items():
            if k not in out or v is not None:
                out[k] = v
    return out
