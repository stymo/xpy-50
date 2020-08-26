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


def parse_int_minus_63_offset(xs:List[str]) -> int:
    x = xs[0]
    return int(x, 16) -63


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
    # --------
    11 + HEADER_LEN: ParamDecoder('VELOCITY_CROSS_FADE', parse_int_zero_offset),
    12 + HEADER_LEN: ParamDecoder('VELOCITY_RANGE_LOWER', parse_int_one_offset),
    13 + HEADER_LEN: ParamDecoder('VELOCITY_RANGE_UPPER', parse_int_one_offset),
    14 + HEADER_LEN: ParamDecoder('KEYBOARD_RANGE_LOWER', parse_int_zero_offset),
    15 + HEADER_LEN: ParamDecoder('KEYOBARD_RANGE_UPPER', parse_int_zero_offset),
    16 + HEADER_LEN: ParamDecoder('REDAMPER_CONTROL_SWITCH', parse_int_zero_offset),
    17 + HEADER_LEN: ParamDecoder('VOLUME_CONTROL_SWITCH', parse_int_one_offset),
    18 + HEADER_LEN: ParamDecoder('HOLD_1_CONTROL_SWITCH', parse_int_one_offset),
    19 + HEADER_LEN: ParamDecoder('BENDER_CONTROL_SWITCH', parse_int_zero_offset),
    20 + HEADER_LEN: ParamDecoder('PAN_CONTROL_SWITCH', parse_int_zero_offset),
    21 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_1', parse_int_zero_offset),
    22 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_1', parse_int_minus_63_offset),
    23 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_2', parse_int_zero_offset),
    24 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_2', parse_int_minus_63_offset),
    25 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_3', parse_int_zero_offset),
    26 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_3', parse_int_minus_63_offset),
    26 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_4', parse_int_zero_offset),
    28 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_4', parse_int_minus_63_offset),
    29 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_1', parse_int_zero_offset),
    30 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_1', parse_int_minus_63_offset),
    31 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_2', parse_int_zero_offset),
    32 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_2', parse_int_minus_63_offset),
    33 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_3', parse_int_zero_offset),
    34 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_3', parse_int_minus_63_offset),
    35 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_4', parse_int_zero_offset),
    36 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_4', parse_int_minus_63_offset),
    37 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_1', parse_int_zero_offset),
    38 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_1', parse_int_minus_63_offset),
    39 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_2', parse_int_zero_offset),
    40 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_2', parse_int_minus_63_offset),
    41 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_3', parse_int_zero_offset),
    42 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_3', parse_int_minus_63_offset),
    43 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_4', parse_int_zero_offset),
    44 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_4', parse_int_minus_63_offset),
    # --------
    45 + HEADER_LEN: ParamDecoder('LFO_1_WAVEFORM', parse_int_zero_offset),
    46 + HEADER_LEN: ParamDecoder('LFO_1_KEY_SYNC', parse_int_zero_offset),
    47 + HEADER_LEN: ParamDecoder('LFO_1_RATE', parse_int_zero_offset),
    48 + HEADER_LEN: ParamDecoder('LFO_1_OFFSET', parse_int_zero_offset),
    49 + HEADER_LEN: ParamDecoder('LFO_1_DELAY_TIME', parse_int_zero_offset),
    50 + HEADER_LEN: ParamDecoder('LFO_1_FADE_MODE', parse_int_zero_offset),
    51 + HEADER_LEN: ParamDecoder('LFO_1_FADE_TIME', parse_int_zero_offset),
    52 + HEADER_LEN: ParamDecoder('LFO_1_EXTERNAL_SYNC', parse_int_zero_offset),
    53 + HEADER_LEN: ParamDecoder('LFO_2_WAVEFORM', parse_int_zero_offset),
    54 + HEADER_LEN: ParamDecoder('LFO_2_KEY_SYNC', parse_int_zero_offset),
    55 + HEADER_LEN: ParamDecoder('LFO_2_RATE', parse_int_zero_offset),
    56 + HEADER_LEN: ParamDecoder('LFO_2_OFFSET', parse_int_zero_offset),
    57 + HEADER_LEN: ParamDecoder('LFO_2_DELAY_TIME', parse_int_zero_offset),
    58 + HEADER_LEN: ParamDecoder('LFO_2_FADE_MODE', parse_int_zero_offset),
    59 + HEADER_LEN: ParamDecoder('LFO_2_FADE_TIME', parse_int_zero_offset),
    60 + HEADER_LEN: ParamDecoder('LFO_2_EXTERNAL_SYNC', parse_int_zero_offset),
    # --------
    # TODO: will need more offset functions... maybe make one offset func, with default of positive 1?
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
