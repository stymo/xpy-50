import csv
import itertools
import glob
from typing import Dict, Iterator, OrderedDict
from typing import Iterator, Dict, Mapping, Any, Union

from src.parsers.sysex_parser import ParamDict


def from_field(val:str) -> Union[int,str]:
    # for now, kind of hacky
    try:
        return int(val)
    except ValueError:
        return str(val)

def from_row(rowdict: Dict[str,str]) -> ParamDict:
    return dict((k,from_field(v)) for k, v in rowdict.items())


def to_row(param_d: ParamDict) -> Dict[str, str]:
    return dict((k, str(v)) for k, v in param_d.items())


# TODO: seperate parser for common and tone files?
def from_file(filepath: str) -> Iterator[ParamDict]:
    with open(filepath, 'r') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield from_row(row)


# def get_patchdata_common(filepath: str) -> Iterator[ParamDict]:
def get_patchdata_all_common(filepath: str) -> Any:  # need vague type to keep mypy happy for some reason
    data_files = glob.glob(filepath + '*_common.csv')
    return itertools.chain.from_iterable(from_file(filepath)
        for filepath in data_files)


# def get_patchdata_all_tones(filepath: str) -> Any:  # need vague type to keep mypy happy for some reason
def get_patchdata_all_tones(filepath):
    data_files = glob.glob(filepath + '*_tones.csv')
    return itertools.chain.from_iterable(from_file(filepath)
        for filepath in data_files)

