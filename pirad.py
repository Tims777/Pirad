#!/usr/bin/env python3

from player import RadioPlayer
from remotecontrol import RemoteControlSocket


if __name__ == '__main__':
    player = RadioPlayer()
    rc = RemoteControlSocket(player)

    try:
        player.play()
        rc.run_forever()
    except KeyboardInterrupt:
        pass
