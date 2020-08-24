import mido # type:ignore

def load_patches(path_to_syx_file):
    # TODO: config
    with mido.open_output('Scarlett 18i8 USB') as ioport:
        for m in mido.read_syx_file(path_to_syx_file):
            ioport.send(m)

