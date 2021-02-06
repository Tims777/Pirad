#!/usr/bin/env python3

import asyncio

from player import RadioPlayer
from remotecontrol import RemoteControlSocket


if __name__ == '__main__':
    player = RadioPlayer()
    rc = RemoteControlSocket(player)

    try:
        player.play()
        start_server = rc.serve(host='', port=7777)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        player.stop()
