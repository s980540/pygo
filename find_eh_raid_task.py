import os
import re
import process_log as pl
import pandas as pd
import argparse
import logging


def split_path_name_ext(file_path: str):
    """Splits the provided file path into its directory, file name, and
    extension components.

    Args:
        file_path (str): The full path of the file to be split.

    Returns:
        tuple: A tuple containing three elements:
            - path (str): The directory path of the file.
            - name (str): The base name of the file without its extension.
            - ext (str): The file extension including the dot (e.g., '.log').
    """
    path = os.path.dirname(file_path)
    name, ext = os.path.splitext(os.path.basename(file_path))
    return path, name, ext


def find_eh_raid_task(file_path: str) -> None:
    """Processes a log file to find specific EH-RAID task entries, extracts
    relevant data, transforms it, and saves it to a CSV file.

    Args:
        file_path (str): The full path of the log file to be processed.
    """
    if not os.path.isfile(file_path):
        logging.error(f"File does not exist: {file_path}")
        return

    try:
        # Read the log file
        with open(file_path, "r", encoding='utf-8', errors='ignore') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return

    # Define the pattern to match the specific log line format
    pattern = re.compile(r"\[.*?\] EH-RAID-Task:(\w+) (\w+) (\w+) (\w+)")

    # List to store the extracted values as tuples
    data = []

    # Iterate over each line in the log file and match the pattern
    for line in lines:
        match = pattern.search(line)
        if match:
            desc_id = match.group(1)    # Extract descriptor ID
            cb_id   = match.group(2)    # Extract callback ID
            faa     = match.group(3)    # Extract FAA field
            status  = match.group(4)    # Extract status
            data.append((desc_id, cb_id, faa, status))

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=["desc_id", "cb_id", "faa", "status"])

    # Apply a transformation to the FAA field and expand it into multiple columns
    try:
        new_columns = ["block", "page", "die", "plane", "frag"]
        df[new_columns] = df["faa"].apply(lambda x: pd.Series(pl.faa_to_tuple(x)))
    except Exception as e:
        logging.error(f"Error processing FAA data: {e}")
        return

    # Remove duplicate 'faa' values
    df = df.drop_duplicates(subset=["faa"])

    lun_shift = 1
    ce_shift = 2
    ch_shift = 2

    try:
        new_columns = ["lun", "ce", "ch"]
        df[new_columns] = df["die"].apply(
            lambda x: pd.Series(pl.die_to_tuple(x, lun_shift, ce_shift, ch_shift))
        )
    except Exception as e:
        logging.error(f"Error processing DIE data: {e}")
        return

    # Split the file path into directory, base name, and extension
    directory, file_name, ext = split_path_name_ext(file_path)

    # Define the path to save the CSV file
    outfile_path = os.path.join(directory, f"{file_name}.csv")

    # Save the DataFrame to a CSV file
    try:
        df.to_csv(outfile_path, index=False)
    except IOError as e:
        logging.error(f"Error saving CSV file {outfile_path}: {e}")
        return

    # Display the DataFrame
    print(df)

    # Provide the file path for downloading
    print(f"File saved to: {outfile_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(description="Find EH-RAID-TASK")
    parser.add_argument(
        "-f",
        "--file",
        dest="file_path",
        help="The full path of the log file to be processed",
        required=True,
    )

    args = parser.parse_args()
    find_eh_raid_task(args.file_path)
