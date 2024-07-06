import re
from collections import defaultdict, OrderedDict


def die_to_tuple(die: str, lun_shift, ce_shift, ch_shift) -> tuple:
    """Convert die value to a tuple of lun, ce, and ch.

    Args:
        die (str): Die value as a hexadecimal string.
        lun_shift (int): Number of bits for lun shift.
        ce_shift (int): Number of bits for ce shift.
        ch_shift (int): Number of bits for ch shift.

    Returns:
        tuple: A tuple containing lun, ce, and ch values as hexadecimal strings.
    """
    die_shift = lun_shift + ce_shift + ch_shift
    bit = bin(int(die, 16))[2:].zfill(die_shift)
    bs = 0
    be = lun_shift
    if lun_shift > 0:
        lun = hex(int(bit[bs:be], 2))[2:]
    else:
        lun = 0

    if ce_shift > 0:
        bs = die_shift - ce_shift - ch_shift
        be = die_shift - ch_shift
        ce = hex(int(bit[bs:be], 2))[2:]
    else:
        ce = 0

    bs = die_shift - ch_shift
    be = die_shift
    ch = hex(int(bit[bs:be], 2))[2:]
    return lun, ce, ch


def faa_to_tuple(faa: str) -> tuple:
    """Convert FAA hexadecimal string to a tuple of block, page, die, and frag.

    Args:
        faa (str): FAA hexadecimal string.

    Returns:
        tuple: Tuple containing block, page, die, plane, and frag values as
        hexadecimal strings.
    """
    bit = bin(int(faa, 16))[2:].zfill(32)
    block = hex(int(bit[:13], 2))[2:]
    page = hex(int(bit[13:24], 2))[2:]
    die = hex(int(bit[24:29], 2))[2:]
    plane = hex(int(bit[29:30], 2))[2:]
    frag = hex(int(bit[30:], 2))[2:]
    return block, page, die, plane, frag


def extract_faa(line: str, pos: int) -> int:
    """Extract FAA from a line at a specified position.

    Args:
        line (str): Input line containing FAA.
        pos (int): Position of FAA in the line.

    Returns:
        int: Integer representation of the FAA in hexadecimal.

    Raises:
        IndexError: If pos is out of range for line.split().
        ValueError: If the extracted FAA cannot be converted to an integer.
    """
    try:
        faa = line.split()[pos]
        return int(faa, 16)
    except IndexError:
        raise IndexError(f"Position {pos} is out of range for line: {line}")
    except ValueError:
        raise ValueError(f"Cannot convert FAA to integer: {faa}")


def filter_lines_by_diff_len(lines: list[str], diff: int) -> list[str]:
    """Filter lines based on their length difference from the average length.

    Args:
        lines (list[str]): List of input lines.
        diff (int): Maximum allowed difference from the average length.

    Returns:
        list[str]: Filtered list of lines.
    """
    avg_len = int(sum(len(line.strip("\\n")) for line in lines) / len(lines))
    filtered_lines = [
        line for line in lines if abs(len(line.strip("\\n")) - avg_len) <= diff
    ]
    return filtered_lines


def filter_line_by_len(lines: list[str], length: int = 0) -> list[str]:
    """Filter lines based on their lengths.

    Args:
        lines (list[str]): List of input lines.
        length (int, optional): Minimum length threshold. Defaults to 0.

    Returns:
        list[str]: Filtered list of lines.
    """
    filtered_lines = [line for line in lines if abs(len(line.strip("\\n"))) == length]
    return filtered_lines


def count_frags(lines: list[str], faa_dict: defaultdict) -> defaultdict:
    """Count occurrences of FAAs in lines and store in a nested defaultdict.

    Args:
        lines (list[str]): List of input lines.
        faa_dict (defaultdict): Nested defaultdict to store counts of FAAs.

    Returns:
        defaultdict: Updated faa_dict with FAA counts.

    Raises:
        ValueError: If the line format does not match the expected pattern.
    """
    for line in lines:
        match = re.search(r"\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)", line)
        if match:
            block = match.group(1)
            page = match.group(2)
            die = match.group(3)
            frag = match.group(4)

            if page not in faa_dict[block]:
                faa_dict[block][page] = defaultdict(lambda: 0)

            if die not in faa_dict[block][page]:
                faa_dict[block][page][die] = 0

            faa_dict[block][page][die] += 1
        else:
            raise ValueError(f"Line '{line.strip()}' does not match expected format.")

    return faa_dict


if __name__ == "__main__":
    die_value = "10"
    lun, ce, ch = die_to_tuple(die_value, 1, 2, 2)
    print(lun, ce, ch)
