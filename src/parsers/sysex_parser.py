import binascii
from typing import List, Dict, Callable, Optional, Tuple, Iterator, Union, NamedTuple

# should be messages_per_patch?
ROWS_PER_PATCH = 5

# ParamToVal?
ParamDict = Dict[str, Union[int,str,None]]

# ParamToParser = Dict[str, Callable[[str], Union[int, str, None]]]

DecoderFunc = Callable[[List[str]], Union[int, str, None]]

# TODO: eventually add other Callable that will be to_onehot?
# holds information needed to decode a parameter
class ParamDecoder(NamedTuple):
    name: str
    decoder: DecoderFunc
    length: int = 1

# maps an offset (byte number) to the corresponding ParamDecoder
OffToDec = Dict[int, ParamDecoder]

# stub for type checking
class SysexMessage:
    def hex(self) -> str:
        pass


def identity(xs: List[str]) -> str:
    x = xs[0]
    return x

# TODO: refactor so each of these takes a list of strings, but normal case will be of len one. could use assertions for that...
# then parser for 2 byte params can have full string: have to rejoin list and extract last chars...
def parse_int_one_offset(xs:List[str]) -> int:
    x = xs[0]
    return int(x, 16) + 1


def parse_int_zero_offset(xs:List[str]) -> int:
    x = xs[0]  # TODO: replace w/ decorator?
    return int(x, 16)


# TODO: ultimately this should be an enum type?
def parse_patch_offset_address(xs:List[str]) -> str:
    x = xs[0]
    d = {'00': 'COMMON',
         '10': 'TONE_1',
         '12': 'TONE_2',
         '14': 'TONE_3',
         '16': 'TONE_4'
        }
    return d[x]


def unhexlify(xs:List[str]) -> str:
    x = xs[0]
    return str(binascii.unhexlify(x), 'utf-8')


def parse_two_bytes_one_offset(xs:List[str]) -> int:
    return int(''.join(map(lambda x: x[1], xs)), 16) + 1


HEADER_PARAM_TO_DECODER: OffToDec = {
    6: ParamDecoder('PATCH_NUMBER', parse_int_one_offset),
    7: ParamDecoder('PATCH_OFFSET_ADDRESS', parse_int_zero_offset),
}


HEADER_LEN = 9

COMMON_PARAM_TO_DECODER: OffToDec = {
        0 + HEADER_LEN: ParamDecoder('PATCH_NAME_1', unhexlify),
        1 + HEADER_LEN: ParamDecoder('PATCH_NAME_2', unhexlify),
        2 + HEADER_LEN: ParamDecoder('PATCH_NAME_3', unhexlify),
        3 + HEADER_LEN: ParamDecoder('PATCH_NAME_4', unhexlify),
        4 + HEADER_LEN: ParamDecoder('PATCH_NAME_5', unhexlify),
        5 + HEADER_LEN: ParamDecoder('PATCH_NAME_6', unhexlify),
        6 + HEADER_LEN: ParamDecoder('PATCH_NAME_7', unhexlify),
        7 + HEADER_LEN: ParamDecoder('PATCH_NAME_8', unhexlify),
        8 + HEADER_LEN: ParamDecoder('PATCH_NAME_9', unhexlify),
        9 + HEADER_LEN: ParamDecoder('PATCH_NAME_10', unhexlify),
        10 + HEADER_LEN: ParamDecoder('PATCH_NAME_11', unhexlify),
        11 + HEADER_LEN: ParamDecoder('PATCH_NAME_12', unhexlify),
        46 + HEADER_LEN: ParamDecoder('PATCH_LEVEL', parse_int_zero_offset),
        68 + HEADER_LEN: ParamDecoder('STRUCTURE_TYPE_1_2', parse_int_one_offset),
        70 + HEADER_LEN: ParamDecoder('STRUCTURE_TYPE_3_4', parse_int_one_offset),
}


TONE_PARAM_TO_DECODER: OffToDec = {
    0 + HEADER_LEN: ParamDecoder('TONE_SWITCH', parse_int_zero_offset),
    1 + HEADER_LEN: ParamDecoder('WAVE_GROUP_TYPE', parse_int_zero_offset),
    2 + HEADER_LEN: ParamDecoder('WAVE_GROUP_ID', parse_int_zero_offset),
    3 + HEADER_LEN: ParamDecoder('WAVE_GROUP_NUMBER_WORD', parse_two_bytes_one_offset, 2),
    5 + HEADER_LEN: ParamDecoder('WAVE_GAIN', parse_int_zero_offset),
    6 + HEADER_LEN: ParamDecoder('FXM_SWITCH', parse_int_zero_offset),
    7 + HEADER_LEN: ParamDecoder('FXM_COLOR', parse_int_one_offset),
    8 + HEADER_LEN: ParamDecoder('FXM_DEPTH', parse_int_one_offset),
    9 + HEADER_LEN: ParamDecoder('TONE_DELAY_MODE', parse_int_zero_offset),
    10 + HEADER_LEN: ParamDecoder('TONE_DELAY_TIME', parse_int_zero_offset),
}


def chunk_sysex_msgs(msgs: List[SysexMessage]) -> Iterator[List[SysexMessage]]:
    N = len(msgs)
    for chunk_start in range(0, N, ROWS_PER_PATCH):
        chunk_end = chunk_start + ROWS_PER_PATCH
        yield msgs[chunk_start:chunk_end]


def from_sysex_msg(msg: SysexMessage, off_to_dec: OffToDec) -> ParamDict:
    # TODO: add validation that offset is within range based on whether this is a tone or common message
    msg_split: List[str] = msg.hex().split()
    d = {}
    for offset, param_decoder in off_to_dec.items():
        d.update({param_decoder.name: param_decoder.decoder(msg_split[offset: offset + param_decoder.length])})
    return d


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
