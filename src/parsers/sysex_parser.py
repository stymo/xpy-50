import binascii
from typing import List, Dict, Callable, Optional, Tuple, Iterator, Union


ParamDict = Dict[str, Union[int,str,None]]

# stub for type checking
class SysexMessage:
    def hex(self) -> str:
        pass


HEADER_KEYS: List[str] = [
    '', # TODO
    '',
    '',
    '',
    '',
    '',
    'PATCH_NUMBER',
    'PATCH_OFFSET_ADDRESS',
    '',
    ]

PARAMS_COMMON_KEYS: List[str] = [
    'PATCH_NAME_1',
    'PATCH_NAME_2',
    'PATCH_NAME_3',
    'PATCH_NAME_4',
    'PATCH_NAME_5',
    'PATCH_NAME_6',
    'PATCH_NAME_7',
    'PATCH_NAME_8',
    'PATCH_NAME_9',
    'PATCH_NAME_10',
    'PATCH_NAME_11',
    'PATCH_NAME_12',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    'PATCH_LEVEL',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    'STRUCTURE_TYPE_1_2',
    '',
    'STRUCTURE_TYPE_3_4',
    ]

PARAMS_TONE_KEYS: List[str] = [
    'TONE_SWITCH',
    ]

# should be messages_per_patch?
ROWS_PER_PATCH = 5


def parse_int_one_offset(x:str) -> int:
    return int(x, 16) + 1


def parse_int_zero_offset(x:str) -> int:
    return int(x, 16)


# TODO: ultimately this should be an enum type?
def parse_patch_offset_address(x:str) -> str:
    d = {'00': 'COMMON',
         '10': 'TONE_1',
         '12': 'TONE_2',
         '14': 'TONE_3',
         '16': 'TONE_4'
        }
    return d[x]

parsers_map: Dict[str, Callable[[str], Union[int, str, None]]] = {
    '': lambda x: None,
    # HEADER
    'PATCH_NUMBER': parse_int_one_offset,
    'PATCH_OFFSET_ADDRESS': parse_patch_offset_address,
    # COMMON
    'PATCH_LEVEL': parse_int_zero_offset,
    'STRUCTURE_TYPE_1_2': parse_int_one_offset,
    'STRUCTURE_TYPE_3_4': parse_int_one_offset,
    # TONE
    'TONE_SWITCH': parse_int_zero_offset,
}


def chunk_sysex_msgs(msgs: List[SysexMessage]) -> Iterator[List[SysexMessage]]:
    N = len(msgs)
    for chunk_start in range(0, N, ROWS_PER_PATCH):
        chunk_end = chunk_start + ROWS_PER_PATCH
        yield msgs[chunk_start:chunk_end]


def from_sysex_msg(msg: SysexMessage, keys: List[str]) -> ParamDict:
    com_data_hex = ((k,v) for k, v in zip(keys, msg.hex().split()))
    # TODO: add assertion here we are looking at correct data address? conditional on comm or tone
    # for now, assume any param w/out assigned parser is an ascii char
    default_func = lambda x: str(binascii.unhexlify(x), 'utf-8')
    return {k: parsers_map.get(k, default_func)(v) for k, v in com_data_hex}


def parse_patch_messages(patch_messages: List[SysexMessage]) -> Iterator[ParamDict]:
    assert len(patch_messages) == 5, "expects list of exactly 5 messages"
    com_msg = patch_messages[0]
    tone_messages = patch_messages[1:5]
    yield from_sysex_msg(com_msg, HEADER_KEYS+PARAMS_COMMON_KEYS)
    for tone_msg in tone_messages:
        yield from_sysex_msg(tone_msg, HEADER_KEYS+PARAMS_TONE_KEYS)

