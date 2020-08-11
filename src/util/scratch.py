# type: ignore

import mido
from mido import Message


# listen
with mido.open_input('Scarlett 18i8 USB') as inport:
    for message in inport:
        print(message)

# send message
ioport = mido.open_output('Scarlett 18i8 USB')
msg = Message("note_on", note=60)
ioport.send(msg)
msg = Message("note_off", note=60)
ioport.send(msg)


# binary note on message
msg_noteon = mido.parse([0x90, 0x3E, 0x5F])

# crazy sysex message to set reverb type
sysex_rev = mido.parse([0xF0, 0x41, 0x10, 0x6A, 0x12, 0x01, 0x00, 0x00, 0x28, 0x06, 0x51, 0xF7])
ioport.send(sysex_rev)

# test turning a tone off and on...
msg = mido.parse([0xF0,
                  0x41,
                  0x10,
                  0x6A,
                  0x12,
                  0x03,  # address start
                  0x00,
                  0x10,
                  0x00,
                  0x00,  # data 0/1
                  0x7C,  # checksum
                  0xF7])

msg = mido.parse([0xF0,
                  0x41,
                  0x10,
                  0x6A,
                  0x12,  # command
                  0x03,  # address start
                  0x00,
                  0x10,
                  0x00,
                  0x01,  # data 0/1
                  0x7B,  # checksum
                  0xF7])


# Try setting 2 tones at once

# try retreiving all info for a patch

# specifically pulling out the tone switches

# try pulling that info directy from a sysex file



# hmmm we seemed to ignore the checksum... 50 vs 51 in second to last byte
sysex_bad = mido.parse([0xF0, 0x41, 0x10, 0x6A, 0x12, 0x01, 0x00, 0x00, 0x28, 0x06, 0x50, 0xF7])

# test querying device
sysex_retr = mido.parse([0xF0, 0x41, 0x10, 0x6A, 0x11, 0x10, 0x02, 0x12, 0x00, 0x00, 0x00, 0x00, 0x19, 0x43, 0xF7])
ioport.send(sysex_retr)
recv_msg = ioport.receive()

ioport.send(msg)

# just in case:
ioport.reset()

ioport.panic()

"""
# Juno
# Filter cuttoff freq
# Params are 0-15
sysex data=(65,50,0,5,0-127) time=0
# Filter res
sysex data=(65,50,0,6,0-127) time=0

# switches
# Square on
sysex data=(65,50,0,16,42) time=0
# Square off
sysex data=(65,50,0,16,34) time=0
# Saw on
sysex data=(65,50,0,16,58) time=0
# Saw off - why is this same as square on?
sysex data=(65,50,0,16,42) time=0

# manual pressed w/ sub 127
sysex data=(65,49,0,0,16,37,15,12,0,57,50,17,30,27,55,28,63,43,70,127,58,24) time=0
# manual pressed w/ sub 0
sysex data=(65,49,0,0,16,37,15,12,0,57,49,17,30,27,55,28,63,43,70,0,58,24) time=0
# manual pressed w/ freq cutoff 127
sysex data=(65,49,0,0,16,37,15,12,0,127,50,17,30,27,55,28,63,43,70,0,58,24) time=0
# manual pressed w/ freq cuttoff 0
sysex data=(65,49,0,0,16,37,15,12,0,0,49,17,30,27,55,28,63,43,70,0,58,24) time=0


TODO:
figure out how to read any/ all params we care about
    - read output from pressing "manual"
can we send mutliple sysex messages at once?
    - no, loop through messages
handle switches

# To load sysex file to synth
messages = mido.read_syx_file('../xp50-sounds/' + filename)

In [287]: for m in messages:
     ...:     ioport.send(m)
     ...:

# print patch number (0-offset) if structure is non-default
In [41]: messages = mido.read_syx_file('data/sysex/CONTRIB.SYX')
In [42]: for i in range(0, len(messages), 5):
    ...:     if int(messages[i].hex().split()[9+0x44], 16) != 0 or int(messages[i].hex().split()[9+0x46], 16) != 0:
    ...:         print(int(messages[i].hex().split()[6], 16))
    ...:
2
3
6
7
8
12
17
22
29
30
32
41
43
44
46
50
52
60
61

"""

{k: v for k, v in zip(HEADER_KEYS+PARAMS_COMMON_KEYS, messages[12*5].hex().split())}

d_1 = {k: parsers_map[k](v) for k, v in d.items()}



