from itertools import groupby

from src.config import DATA_CSV_DIR
from src.data_loaders.csv import get_patchdata_all_common, get_patchdata_all_tones

def get_total_num_tones() -> int:
    """
    Returns the total number of active tones in the data set
    """
    csv_filepath = DATA_CSV_DIR
    data = get_patchdata_all_tones(csv_filepath)
    return sum(x['TONE_SWITCH'] for x in data)


def get_total_num_patches() -> int:
    """
    Returns the total number of patches in the data set
    """
    csv_filepath = DATA_CSV_DIR
    data = get_patchdata_all_tones(csv_filepath)
    # note: this relies on assumption that patches are grouped by patch number in sysex
    # file and the fact that Pythobn's group by will not group patches having
    # the same number that are not adjacent in input (so in different sysex files)
    data_grouped = groupby(data, key=lambda x: x['PATCH_NUMBER'])
    return len(list(data_grouped))

