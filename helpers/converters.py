def hex_str_to_bin_str(hex: str) -> str:
    # https://stackoverflow.com/questions/1425493/convert-hex-to-binary/28913296#28913296
    return bin(int(hex, 16))[2:].zfill(len(hex) * 4)