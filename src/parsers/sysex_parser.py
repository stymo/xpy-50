import binascii
from typing import List, Dict, Callable, Optional, Tuple, Iterator, Union

# should be messages_per_patch?
ROWS_PER_PATCH = 5

# ParamToVal?
ParamDict = Dict[str, Union[int,str,None]]

ParamToParser = Dict[str, Callable[[str], Union[int, str, None]]]


# TODO: eventually add other Callable that will be to_onehot?
# maps a parameter name to a function that decodes it from the sysex message
ParamDecoder = Tuple[str, Callable[[str], Union[int, str, None]]]

# maps an offset (byte number) to the corresponding ParamDecoder
OffToDec = Dict[int, ParamDecoder]



# stub for type checking
class SysexMessage:
    def hex(self) -> str:
        pass


def identity(x: str) -> str:
    return x


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


HEADER_PARAM_TO_DECODER: OffToDec = {
    6: ('PATCH_NUMBER', parse_int_one_offset),
    7: ('PATCH_OFFSET_ADDRESS', parse_int_zero_offset),
}


def unhexlify(s: str) -> str:
    return str(binascii.unhexlify(s), 'utf-8')


HEADER_LEN = 9

COMMON_PARAM_TO_DECODER: OffToDec = {
        0 + HEADER_LEN: ('PATCH_NAME_1', unhexlify),
        1 + HEADER_LEN: ('PATCH_NAME_2', unhexlify),
        2 + HEADER_LEN: ('PATCH_NAME_3', unhexlify),
        3 + HEADER_LEN: ('PATCH_NAME_4', unhexlify),
        4 + HEADER_LEN: ('PATCH_NAME_5', unhexlify),
        5 + HEADER_LEN: ('PATCH_NAME_6', unhexlify),
        6 + HEADER_LEN: ('PATCH_NAME_7', unhexlify),
        7 + HEADER_LEN: ('PATCH_NAME_8', unhexlify),
        8 + HEADER_LEN: ('PATCH_NAME_9', unhexlify),
        9 + HEADER_LEN: ('PATCH_NAME_10', unhexlify),
        10 + HEADER_LEN: ('PATCH_NAME_11', unhexlify),
        11 + HEADER_LEN: ('PATCH_NAME_12', unhexlify),
        46 + HEADER_LEN: ('PATCH_LEVEL', parse_int_zero_offset),
        68 + HEADER_LEN: ('STRUCTURE_TYPE_1_2', parse_int_one_offset),
        70 + HEADER_LEN: ('STRUCTURE_TYPE_3_4', parse_int_one_offset),
}


PARAMS_TONE: ParamToParser = {
    'TONE_SWITCH': parse_int_zero_offset,
    'WAVE_GROUP_TYPE': identity,
    'WAVE_GROUP_ID': identity,
    'WAVE_GROUP_NUMBER_WORD_1': identity,
    'WAVE_GROUP_NUMBER_WORD_2': identity,
    'WAVE_GAIN': identity,
    'FXM_SWITCH': identity,
    'FXM_COLOR': identity,
    'FXM_DEPTH': identity,
    'TONE_DELAY_MODE': identity,
    'TONE_DELAY_TIME': identity,
}


TONE_PARAM_TO_DECODER: OffToDec = {
    0 + HEADER_LEN: ('TONE_SWITCH', parse_int_zero_offset),
    1 + HEADER_LEN: ('WAVE_GROUP_TYPE', identity),
    2 + HEADER_LEN: ('WAVE_GROUP_ID', identity),
    3 + HEADER_LEN: ('WAVE_GROUP_NUMBER_WORD_1', identity), # TODO: this will need to read from subsequent param
    4 + HEADER_LEN: ('WAVE_GROUP_NUMBER_WORD_2', identity),
    5 + HEADER_LEN: ('WAVE_GAIN', identity),
    6 + HEADER_LEN: ('FXM_SWITCH', identity),
    7 + HEADER_LEN: ('FXM_COLOR', identity),
    8 + HEADER_LEN: ('FXM_DEPTH', identity),
    8 + HEADER_LEN: ('TONE_DELAY_MODE', identity),
    10 + HEADER_LEN: ('TONE_DELAY_TIME', identity),
}


def chunk_sysex_msgs(msgs: List[SysexMessage]) -> Iterator[List[SysexMessage]]:
    N = len(msgs)
    for chunk_start in range(0, N, ROWS_PER_PATCH):
        chunk_end = chunk_start + ROWS_PER_PATCH
        yield msgs[chunk_start:chunk_end]


def from_sysex_msg(msg: SysexMessage, off_to_dec: OffToDec) -> ParamDict:
    msg_split: List[str] = msg.hex().split()
    return {v[0]: v[1](msg_split[k]) for k, v in off_to_dec.items()}


def parse_patch_messages(patch_messages: List[SysexMessage]) -> Iterator[ParamDict]:
    assert len(patch_messages) == 5, "expects list of exactly 5 messages"
    com_msg = patch_messages[0]
    tone_messages = patch_messages[1:5]
    # TODO: top level variable?
    comm_off_to_dec = {**HEADER_PARAM_TO_DECODER, **COMMON_PARAM_TO_DECODER}
    yield from_sysex_msg(com_msg, comm_off_to_dec)
    tone_off_to_dec = {**HEADER_PARAM_TO_DECODER, **TONE_PARAM_TO_DECODER}
    for tone_msg in tone_messages:
        yield from_sysex_msg(tone_msg, tone_off_to_dec)
