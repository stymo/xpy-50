import csv
import glob
import os.path
from typing import List

import mido  # type: ignore

from src.config import DATA_CSV_DIR, DATA_SYX_DIR
from src.parsers.sysex_parser import parse_patch_messages, PARAMS_COMMON_KEYS, \
    PARAMS_TONE_KEYS, ROWS_PER_PATCH, HEADER_KEYS, chunk_sysex_msgs
from src.data_loaders.csv import to_row


def sysex_file_to_csvs(syx_filepath: str, csv_path: str) -> None:
    with open(syx_filepath, 'r') as syx_file:
        # also open write file for common and tone csvs
        msgs = mido.read_syx_file(syx_filepath)
        file_basename = os.path.splitext(os.path.basename(syx_filepath))[0]
        common_csvfile_name = csv_path + file_basename + '_common.csv'
        tones_csvfile_name = csv_path + file_basename + '_tones.csv'

        with open(common_csvfile_name, 'w') as common_csvfile:
            with open(tones_csvfile_name, 'w') as tones_csvfile:
                # TODO: for now, filter out '' keys
                common_fieldnames = filter(lambda x: x != '', HEADER_KEYS+PARAMS_COMMON_KEYS)
                common_writer = csv.DictWriter(common_csvfile,
                    fieldnames=list(common_fieldnames), extrasaction='ignore')
                tones_fieldnames = filter(lambda x: x != '', HEADER_KEYS+PARAMS_TONE_KEYS)
                tones_writer = csv.DictWriter(tones_csvfile,
                    fieldnames=list(tones_fieldnames), extrasaction='ignore')
                common_writer.writeheader()
                tones_writer.writeheader()

                for patch_msgs in chunk_sysex_msgs(msgs):
                    patch_data_chunks = parse_patch_messages(patch_msgs)
                    com_data = to_row(next(patch_data_chunks))
                    common_writer.writerow(com_data)
                    for tone_data in patch_data_chunks:
                        tones_writer.writerow(to_row(tone_data))


def all_sysex_to_csvs(syx_path: str, csv_path: str):
    syx_files = glob.glob(DATA_SYX_DIR + '*.SYX')
    for x in syx_files:
        sysex_file_to_csvs(x, csv_path)

if __name__ == '__main__':
    # for now, just test on one file
    # sysex_file_to_csvs('data/sysex/CONTRIB.SYX', 'data/csv/CONTRIB')

    all_sysex_to_csvs(DATA_SYX_DIR, DATA_CSV_DIR)

