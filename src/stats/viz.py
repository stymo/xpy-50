from collections import Counter
from itertools import groupby
import typing
from typing import List

import matplotlib.pyplot as plt # type:ignore

from src.config import DATA_CSV_DIR, IMAGES_DIR
from src.parsers.sysex_parser import ParamDict
from src.data_loaders.csv import get_patchdata_all_common, get_patchdata_all_tones


def show_patches_using_each_struct() -> None:
    csv_filepath = DATA_CSV_DIR
    # note that this only checks the structure between tones 1 and 2
    # maybe we should see if any patches use a different structure type between
    # their 1/2 and 3/4 tones?
    histogram = Counter(patch_data['STRUCTURE_TYPE_1_2']
            for patch_data
            in get_patchdata_all_common(csv_filepath))
    # TODO: sort by numeric order or most common?
    plt.bar(histogram.keys(), histogram.values())
    plt.xlabel('Structure Types')
    plt.ylabel('Patches w/ Structure Type')
    # plt.show()
    plt.savefig(IMAGES_DIR + 'patches_using_each_struct.png')
    plt.close()

def show_tones_active_in_patch() -> None:
    """
    For each tone, shows how many patches have that tone active
    """
    csv_filepath = DATA_CSV_DIR
    data = get_patchdata_all_tones(csv_filepath)
    data = map(lambda x: x['PATCH_OFFSET_ADDRESS'],
                filter(lambda x: x['TONE_SWITCH'] == 1, data)
                )
    histogram: typing.Counter[int] = Counter(data)
    plt.bar(histogram.keys(), histogram.values())
    plt.xlabel('Tones')
    plt.ylabel('Patches Having Tone Active')
    # plt.show()
    plt.savefig(IMAGES_DIR + 'tones_active_in_patch.png')
    plt.close()


def show_num_tones_active_in_patch() -> None:
    """
    For each patch, shows how many tones are active
    """
    csv_filepath = DATA_CSV_DIR
    data = get_patchdata_all_tones(csv_filepath)
    # note: this relies on assumption that patches are grouped by patch number in sysex
    # file and the fact that Python's group by will not group patches having
    # the same number that are not adjacent in input (so in different sysex files)
    data_grouped = groupby(data, key=lambda x: x['PATCH_NUMBER'])
    # add up the active tone switches (value of 1) in each patch
    data_mapped = map(lambda tup: sum((x['TONE_SWITCH'] for x in tup[1])), data_grouped)
    histogram = Counter(data_mapped)
    plt.bar(histogram.keys(), histogram.values())
    plt.xlabel('Num Active Tones in Patch')
    plt.ylabel('Patches')
    # plt.show()
    plt.savefig(IMAGES_DIR + 'num_tones_active_in_patch.png')
    plt.close()


if __name__ == '__main__':
    show_patches_using_each_struct()
    show_tones_active_in_patch()
    show_num_tones_active_in_patch()

