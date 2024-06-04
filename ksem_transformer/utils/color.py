def hex_color_to_tuple(hex_color: str) -> tuple[int, int, int]:
    color_int = int(hex_color.removeprefix("#"), base=16)
    return color_int & 0xFF, (color_int >> 8) & 0xFF, color_int >> 16
