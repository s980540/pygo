# process_log.py

import re
from collections import defaultdict, OrderedDict

def faa_to_tuple(faa: str) -> tuple:
    """
    Convert FAA (Fully Associative Address) hexadecimal string to a tuple of block, page, die, and frag.

    Args:
        faa (str): FAA hexadecimal string.

    Returns:
        tuple: Tuple containing block, page, die, and frag values as hexadecimal strings.
    """
    bit = bin(int(faa, 16))[2:].zfill(32)
    block = hex(int(bit[:13], 2))[2:]
    page = hex(int(bit[13:24], 2))[2:]
    die = hex(int(bit[24:29], 2))[2:]
    frag = hex(int(bit[29:], 2))[2:]
    return block, page, die, frag

def extract_faa(line: str, pos: int) -> int:
    """
    Extract FAA (Fully Associative Address) from a line at a specified position.

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
        raise ValueError(f"Failed to convert FAA {faa} to an integer.")

def filter_line_by_diff(lines: list[str], diff: int = 0) -> list[str]:
    """
    Filter lines based on the difference in their lengths compared to the average length.

    Args:
        lines (list[str]): List of input lines.
        diff (int, optional): Maximum allowed difference from average length. Defaults to 0.

    Returns:
        list[str]: Filtered list of lines.
    """
    avg_len = int(sum(len(line.strip('\n')) for line in lines) / len(lines))
    filtered_lines = [line for line in lines if abs(len(line.strip('\n')) - avg_len) <= diff]
    return filtered_lines

def filter_line_by_len(lines: list[str], length: int = 0) -> list[str]:
    """
    Filter lines based on their lengths.

    Args:
        lines (list[str]): List of input lines.
        length (int, optional): Minimum length threshold. Defaults to 0.

    Returns:
        list[str]: Filtered list of lines.
    """
    filtered_lines = [line for line in lines if abs(len(line.strip('\n'))) > length]
    return filtered_lines

def count_frags(lines: list[str], faa_dict: defaultdict) -> defaultdict:
    """
    Count occurrences of FAAs (Fully Associative Addresses) in lines and store in a nested defaultdict.

    Args:
        lines (list[str]): List of input lines.
        faa_dict (defaultdict): Nested defaultdict to store counts of FAAs.

    Returns:
        defaultdict: Updated faa_dict with FAA counts.

    Raises:
        ValueError: If the line format does not match the expected pattern.
    """
    for line in lines:
        match = re.search(r'\(\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\)', line)
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
