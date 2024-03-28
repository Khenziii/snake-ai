from typing import Tuple


def hex_string_to_rgb_tuple(hex_string: str) -> Tuple[int, int, int]:
    try:
        # Remove '#' if present
        hex_code = hex_string.lstrip('#')

        # Convert hex to RGB
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)

        return (r, g, b)
    except Exception as e:
        print("Most likely, an invalid hex was specified in config.json.")
        raise e


def rgb_tuple_to_hex_string(rgb_tuple: Tuple[int, int, int]) -> str:
    # Ensure values are within valid range (0-255)
    r = max(0, min(rgb_tuple[0], 255))
    g = max(0, min(rgb_tuple[1], 255))
    b = max(0, min(rgb_tuple[2], 255))

    hex_string: str = f'#{r:02x}{g:02x}{b:02x}'
    return hex_string


# Expected input example: (0,0,0)
def rgb_string_to_rgb_tuple(rgb_string: str) -> Tuple[int, int, int]:
    if rgb_string[0] == "(" and rgb_string[-1] == ")":
        rgb_string = rgb_string.strip('()')

    str_list = rgb_string.split(',')
    int_list = []

    for string in str_list:
        int_list.append(int(string))

    if len(int_list) > 3 or len(int_list) < 3:
        raise ValueError("rgb_string had more than 3 fields.")

    return (int_list[0], int_list[1], int_list[2])
