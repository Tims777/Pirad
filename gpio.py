#!/usr/bin/env python3

from gpiozero import Button


class ButtonControl():

    def __init__(self, player, pins):
        self.player = player
        self.buttons = [Button(p) for p in pins]
        if len(self.buttons) == 2:
            self.buttons[0].when_pressed = lambda: self.player.switch_station(self.player.station_id + 1)
            self.buttons[1].when_pressed = lambda: self.player.switch_station(self.player.station_id - 1)
        else:
            raise NotImplementedError("Currently only a two-button-layout is supported.")
