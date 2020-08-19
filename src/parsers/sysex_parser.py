import binascii
from typing import List, Dict, Callable, Optional, Tuple, Iterator, Union

# should be messages_per_patch?
ROWS_PER_PATCH = 5

# ParamToVal?
ParamDict = Dict[str, Union[int,str,None]]

ParamToParser = Dict[str, Callable[[str], Union[int, str, None]]]

# stub for type checking
class SysexMessage:
    def hex(self) -> str:
        pass

# TODO: replace with map to parser. may want to update map to named tuple that
# will include word offset so we don't need entry for params we don't care about
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

parsers_map: ParamToParser = {
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

HEADER_TO_PARSER: ParamToParser = {
    'WORD_0': identity,
    'WORD_1': identity,
    'WORD_2': identity,
    'WORD_3': identity,
    'WORD_4': identity,
    'WORD_5': identity,
    'PATCH_NUMBER': parse_int_one_offset,
    'PATCH_OFFSET_ADDRESS': parse_int_zero_offset,
    'WORD_8': identity
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


def from_sysex_msg_tone(msg: SysexMessage, params: ParamToParser) -> ParamDict:
    param_data_hex = ((m,v) for m, v in zip(params.items(), msg.hex().split()))
    return {m[0]: m[1](v) for m, v in param_data_hex}


def parse_patch_messages(patch_messages: List[SysexMessage]) -> Iterator[ParamDict]:
    assert len(patch_messages) == 5, "expects list of exactly 5 messages"
    com_msg = patch_messages[0]
    tone_messages = patch_messages[1:5]
    yield from_sysex_msg(com_msg, list(HEADER_TO_PARSER.keys())+PARAMS_COMMON_KEYS)
    for tone_msg in tone_messages:
        # TODO: `params` needs to be header and tone params as dict
        tone_params = dict()
        tone_params.update(HEADER_TO_PARSER)
        tone_params.update(PARAMS_TONE)
        yield from_sysex_msg_tone(tone_msg, tone_params)
