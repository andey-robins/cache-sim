def hex_str_to_bin_str(hex: str) -> str:
    # https://stackoverflow.com/questions/1425493/convert-hex-to-binary/28913296#28913296
    # additional padding logic mine, since we assume a full 32 bits will
    # be provided from this function every time
    s = bin(int(hex, 16))[2:].zfill(len(hex) * 4)
    return "0" * (32 - len(s)) + s