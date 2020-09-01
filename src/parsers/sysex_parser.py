import binascii
from typing import List, Dict, Callable, Optional, Tuple, Iterator, Union, NamedTuple, Optional

# should be messages_per_patch?
ROWS_PER_PATCH = 5

# ParamToVal?
ParamDict = Dict[str, Union[int,str,None]]

# ParamToParser = Dict[str, Callable[[str], Union[int, str, None]]]

# DecoderFunc = Callable[[List[str], int], Union[int, str, None]]
DecoderFunc = Callable[[List[str], Optional[int]], Union[int, str, None]]
# DecoderFunc = Callable[Union[[List[str], int], [List[str]]], Union[int, str, None]]

# TODO: eventually add other Callable that will be to_onehot?
# holds information needed to decode a parameter
class ParamDecoder(NamedTuple):
    name: str
    decoder: DecoderFunc
    length: int = 1
    offset: int = 0

# maps an offset (byte number) to the corresponding ParamDecoder
OffToDec = Dict[int, ParamDecoder]

# stub for type checking
class SysexMessage:
    def hex(self) -> str:
        pass

# `args` needed for type checking
def identity(xs: List[str], *args) -> str:
    # TODO: use decorator to get first element?? How does that effect type?
    # TDOO: add assertion of length
    x = xs[0]
    return x


def parse_int(xs:List[str], offset=0) -> int:
    x = xs[0]
    return int(x, 16) + offset


# TODO: ultimately this should be an enum type?
def parse_patch_offset_address(xs:List[str], *args) -> str:
    x = xs[0]
    d = {'00': 'COMMON',
         '10': 'TONE_1',
         '12': 'TONE_2',
         '14': 'TONE_3',
         '16': 'TONE_4'
        }
    return d[x]


def unhexlify(xs:List[str], *args) -> str:
    x = xs[0]
    return str(binascii.unhexlify(x), 'utf-8')


def parse_two_bytes_one_offset(xs:List[str], *args) -> int:
    return int(''.join(map(lambda x: x[1], xs)), 16) + 1


HEADER_PARAM_TO_DECODER: OffToDec = {
    6: ParamDecoder('PATCH_NUMBER', parse_int, offset=1),
    7: ParamDecoder('PATCH_OFFSET_ADDRESS', parse_int),
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
        46 + HEADER_LEN: ParamDecoder('PATCH_LEVEL', parse_int),
        68 + HEADER_LEN: ParamDecoder('STRUCTURE_TYPE_1_2', parse_int, offset=1),
        70 + HEADER_LEN: ParamDecoder('STRUCTURE_TYPE_3_4', parse_int, offset=1),
}


TONE_PARAM_TO_DECODER: OffToDec = {
    0 + HEADER_LEN: ParamDecoder('TONE_SWITCH', parse_int),
    1 + HEADER_LEN: ParamDecoder('WAVE_GROUP_TYPE', parse_int),
    2 + HEADER_LEN: ParamDecoder('WAVE_GROUP_ID', parse_int),
    3 + HEADER_LEN: ParamDecoder('WAVE_GROUP_NUMBER_WORD', parse_two_bytes_one_offset, 2),
    5 + HEADER_LEN: ParamDecoder('WAVE_GAIN', parse_int),
    6 + HEADER_LEN: ParamDecoder('FXM_SWITCH', parse_int),
    7 + HEADER_LEN: ParamDecoder('FXM_COLOR', parse_int, offset=1),
    8 + HEADER_LEN: ParamDecoder('FXM_DEPTH', parse_int, offset=1),
    9 + HEADER_LEN: ParamDecoder('TONE_DELAY_MODE', parse_int),
    10 + HEADER_LEN: ParamDecoder('TONE_DELAY_TIME', parse_int),
    # --------
    11 + HEADER_LEN: ParamDecoder('VELOCITY_CROSS_FADE', parse_int),
    12 + HEADER_LEN: ParamDecoder('VELOCITY_RANGE_LOWER', parse_int, offset=1),
    13 + HEADER_LEN: ParamDecoder('VELOCITY_RANGE_UPPER', parse_int, offset=1),
    14 + HEADER_LEN: ParamDecoder('KEYBOARD_RANGE_LOWER', parse_int),
    15 + HEADER_LEN: ParamDecoder('KEYOBARD_RANGE_UPPER', parse_int),
    16 + HEADER_LEN: ParamDecoder('REDAMPER_CONTROL_SWITCH', parse_int),
    17 + HEADER_LEN: ParamDecoder('VOLUME_CONTROL_SWITCH', parse_int, offset=1),
    18 + HEADER_LEN: ParamDecoder('HOLD_1_CONTROL_SWITCH', parse_int, offset=1),
    19 + HEADER_LEN: ParamDecoder('BENDER_CONTROL_SWITCH', parse_int),
    20 + HEADER_LEN: ParamDecoder('PAN_CONTROL_SWITCH', parse_int),
    21 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_1', parse_int),
    22 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_1', parse_int, offset=-63),
    23 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_2', parse_int),
    24 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_2', parse_int, offset=-63),
    25 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_3', parse_int),
    26 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_3', parse_int, offset=-63),
    26 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DESTINATION_4', parse_int),
    28 + HEADER_LEN: ParamDecoder('CONTROLLER_1_DEPTH_4', parse_int, offset=-63),
    29 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_1', parse_int),
    30 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_1', parse_int, offset=-63),
    31 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_2', parse_int),
    32 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_2', parse_int, offset=-63),
    33 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_3', parse_int),
    34 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_3', parse_int, offset=-63),
    35 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DESTINATION_4', parse_int),
    36 + HEADER_LEN: ParamDecoder('CONTROLLER_2_DEPTH_4', parse_int, offset=-63),
    37 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_1', parse_int),
    38 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_1', parse_int, offset=-63),
    39 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_2', parse_int),
    40 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_2', parse_int, offset=-63),
    41 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_3', parse_int),
    42 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_3', parse_int, offset=-63),
    43 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DESTINATION_4', parse_int),
    44 + HEADER_LEN: ParamDecoder('CONTROLLER_3_DEPTH_4', parse_int, offset=-63),
    # --------
    45 + HEADER_LEN: ParamDecoder('LFO_1_WAVEFORM', parse_int),
    46 + HEADER_LEN: ParamDecoder('LFO_1_KEY_SYNC', parse_int),
    47 + HEADER_LEN: ParamDecoder('LFO_1_RATE', parse_int),
    48 + HEADER_LEN: ParamDecoder('LFO_1_OFFSET', parse_int),
    49 + HEADER_LEN: ParamDecoder('LFO_1_DELAY_TIME', parse_int),
    50 + HEADER_LEN: ParamDecoder('LFO_1_FADE_MODE', parse_int),
    51 + HEADER_LEN: ParamDecoder('LFO_1_FADE_TIME', parse_int),
    52 + HEADER_LEN: ParamDecoder('LFO_1_EXTERNAL_SYNC', parse_int),
    53 + HEADER_LEN: ParamDecoder('LFO_2_WAVEFORM', parse_int),
    54 + HEADER_LEN: ParamDecoder('LFO_2_KEY_SYNC', parse_int),
    55 + HEADER_LEN: ParamDecoder('LFO_2_RATE', parse_int),
    56 + HEADER_LEN: ParamDecoder('LFO_2_OFFSET', parse_int),
    57 + HEADER_LEN: ParamDecoder('LFO_2_DELAY_TIME', parse_int),
    58 + HEADER_LEN: ParamDecoder('LFO_2_FADE_MODE', parse_int),
    59 + HEADER_LEN: ParamDecoder('LFO_2_FADE_TIME', parse_int),
    60 + HEADER_LEN: ParamDecoder('LFO_2_EXTERNAL_SYNC', parse_int),
    # --------
    61 + HEADER_LEN: ParamDecoder('COURSE_TUNE', parse_int, offset=-48),
    62 + HEADER_LEN: ParamDecoder('FINE_TUNE', parse_int, offset=-50),
    63 + HEADER_LEN: ParamDecoder('RANDOM_PITCH_DEPTH', parse_int),
    64 + HEADER_LEN: ParamDecoder('PITCH_KEYFOLLOW', parse_int),
    65 + HEADER_LEN: ParamDecoder('PITCH_ENVELOPE_DEPTH', parse_int, offset=-12),
    66 + HEADER_LEN: ParamDecoder('PITCH_ENV_VEL_SENSE', parse_int),
    67 + HEADER_LEN: ParamDecoder('PITCH_ENV_VEL_TIME_1', parse_int),
    68 + HEADER_LEN: ParamDecoder('PITCH_ENV_VEL_TIME_4', parse_int),
    69 + HEADER_LEN: ParamDecoder('PITCH_ENV_TIME_KEYFOLLOW', parse_int),
    70 + HEADER_LEN: ParamDecoder('PITCH_ENV_TIME_1', parse_int),
    71 + HEADER_LEN: ParamDecoder('PITCH_ENV_TIME_2', parse_int),
    72 + HEADER_LEN: ParamDecoder('PITCH_ENV_TIME_3', parse_int),
    73 + HEADER_LEN: ParamDecoder('PITCH_ENV_TIME_4', parse_int),
    74 + HEADER_LEN: ParamDecoder('PITCH_ENV_LEVEL_1', parse_int, offset=-63),
    75 + HEADER_LEN: ParamDecoder('PITCH_ENV_LEVEL_2', parse_int, offset=-63),
    76 + HEADER_LEN: ParamDecoder('PITCH_ENV_LEVEL_3', parse_int, offset=-63),
    77 + HEADER_LEN: ParamDecoder('PITCH_ENV_LEVEL_4', parse_int, offset=-63),
    78 + HEADER_LEN: ParamDecoder('PITCH_LFO_1_DEPTH', parse_int, offset=-63),
    79 + HEADER_LEN: ParamDecoder('PITCH_LFO_2_DEPTH', parse_int, offset=-63),
    # --------
    80 + HEADER_LEN: ParamDecoder('FILTER_TYPE', parse_int),
    81 + HEADER_LEN: ParamDecoder('CUTOFF_FREQ', parse_int),
    82 + HEADER_LEN: ParamDecoder('CUTOFF_KEYFOLLOW', parse_int),
    83 + HEADER_LEN: ParamDecoder('RESONANCE', parse_int),
    84 + HEADER_LEN: ParamDecoder('RESONANCE_VELOCITY_SENSE', parse_int),
    85 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_DEPTH', parse_int),
    86 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_VELOCITY_CURVE', parse_int),
    87 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_VELOCITY_SENSE', parse_int),
    88 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_VELCOCITY_TIME1', parse_int),
    89 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_VELOCITY_TIME4', parse_int),
    90 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_TIME_KEYFOLLOW', parse_int),
    91 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_TIME_1', parse_int),
    92 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_TIME_2', parse_int),
    93 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_TIME_3', parse_int),
    94 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_TIME_4', parse_int),
    95 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_LEVEL_1', parse_int),
    96 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_LEVEL_2', parse_int),
    97 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_LEVEL_3', parse_int),
    98 + HEADER_LEN: ParamDecoder('FILTER_ENVELOPE_LEVEL_4', parse_int),
    99 + HEADER_LEN: ParamDecoder('FILTER_LFO_1_DEPTH', parse_int, offset=-63),
    100 + HEADER_LEN: ParamDecoder('FILTER_LFO_2_DEPTH', parse_int, offset=-63),
    # --------
    101 + HEADER_LEN: ParamDecoder('TONE_LEVEL', parse_int),
    102 + HEADER_LEN: ParamDecoder('BIAS_DIRECTION', parse_int),
    103 + HEADER_LEN: ParamDecoder('BIAS_POSITION', parse_int),
    104 + HEADER_LEN: ParamDecoder('BIAS_LEVEL', parse_int),
    105 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_VELOCITY_CURVE', parse_int, offset=1),
    106 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_VELOCITY_SENSE', parse_int),
    107 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_VELOCITY_TIME_1', parse_int),
    108 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_VELOCITY_TIME_4', parse_int),
    109 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_VELOCITY_TIME_KEYFOLLOW', parse_int),
    110 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_TIME_1', parse_int),
    111 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_TIME_2', parse_int),
    112 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_TIME_3', parse_int),
    113 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_TIME_4', parse_int),
    114 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_LEVEL_1', parse_int),
    115 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_LEVEL_2', parse_int),
    116 + HEADER_LEN: ParamDecoder('LEVEL_ENVELOPE_LEVEL_3', parse_int),
    117 + HEADER_LEN: ParamDecoder('LEVEL_LFO1_DEPTH', parse_int, offset=-63),
    118 + HEADER_LEN: ParamDecoder('LEVEL_LFO2_DEPTH', parse_int, offset=-63),
    119 + HEADER_LEN: ParamDecoder('TONE_PAN', parse_int),
    120 + HEADER_LEN: ParamDecoder('PAN_KEYFOLLOW', parse_int),
    121 + HEADER_LEN: ParamDecoder('RANDOM_PAN_DEPTH', parse_int),
    122 + HEADER_LEN: ParamDecoder('ALTERNATE_PAN_DEPTH', parse_int, offset=1),
    123 + HEADER_LEN: ParamDecoder('PAN_LFO_1_DEPTH', parse_int),
    124 + HEADER_LEN: ParamDecoder('PAN_LFO_2_DEPTH', parse_int),
    # --------
    125 + HEADER_LEN: ParamDecoder('OUTPUT_ASSIGN', parse_int),
    126 + HEADER_LEN: ParamDecoder('MIX_EFX_SEND_LEVEL', parse_int),
    127 + HEADER_LEN: ParamDecoder('CHORUS_SEND_LEVEL', parse_int),
    128 + HEADER_LEN: ParamDecoder('REVERB_SEND_LEVEL', parse_int),
}


def chunk_sysex_msgs(msgs: List[SysexMessage]) -> Iterator[List[SysexMessage]]:
    N = len(msgs)
    for chunk_start in range(0, N, ROWS_PER_PATCH):
        chunk_end = chunk_start + ROWS_PER_PATCH
        yield msgs[chunk_start:chunk_end]


def from_sysex_msg(msg: SysexMessage, off_to_dec: OffToDec) -> ParamDict:
    # TODO: add validation that offset is within range based on whether this is a tone or common message
    msg_split: List[str] = msg.hex().split() # TODO: make this a dictionary comprehension again
    d = {}
    for offset, param_decoder in off_to_dec.items():
        d.update({param_decoder.name:
            param_decoder.decoder(msg_split[offset:
                offset + param_decoder.length],
                param_decoder.offset
                )})
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
