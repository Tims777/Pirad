#!/usr/bin/env python3

import asyncio

from player import RadioPlayer
from remotecontrol import RemoteControlSocket
from gpio import ButtonControl

# list of acceptable origins
# * this is only to prevent xss-attacks (and does not diallow connections with a "faked" origin)
# * 'null' is sent by firefox instead of 'file://'
origins = ['http://192.168.0.77', 'file://', 'null']  # null is sent for local files opened in the browser

# GPIO pins of the buttons
pins = [17, 18]


if __name__ == '__main__':
    player = RadioPlayer()
    rc = RemoteControlSocket(player)
    bt = ButtonControl(player, pins)

    try:
        player.play()
        start_server = rc.serve(host='', port=7777, origins=origins)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        player.stop()
