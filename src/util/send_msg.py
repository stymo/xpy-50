import mido  # type: ignore
from mido import Message # type: ignore


ioport = mido.open_output('Scarlett 18i8 USB')


def checksum(address=[], data_or_size=[]):
    the_bytes = address + data_or_size
    the_sum = sum(the_bytes)
    remainder = the_sum % 128
    return (hex(128-remainder))


def make_message(command_id, address, data_or_size):
    the_bytes = [0xF0, 0x41, 0x10, 0x6A] \
                + [command_id] \
                + address \
                + data_or_size \
                + [int(checksum(address, data_or_size), 16)] \
                + [0xF7]
    return mido.parse(the_bytes)

# Temp Path Tone 2 on
msg = make_message(0x12, [0x03,0x00,0x12,0x00], [0x01])
# off
msg = make_message(0x12, [0x03,0x00,0x12,0x00], [0x00])

# trying to update tones 2 and 3 at once

ioport.send(msg)
ioport.close()
