import rotaryio

import config


enc = rotaryio.IncrementalEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2)

old_val = new_val = enc.position
while True:
    new_val = enc.position

    if new_val != old_val:
        print(new_val)
        old_val = new_val
