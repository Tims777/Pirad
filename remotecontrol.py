#!/usr/bin/env python3

import os
import sys
import asyncio
import json
import websockets

from utils import parse_change


class RemoteControlSocket():

    connected = set()

    def __init__(self, player):
        self.player = player

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            message = await self.produce()
            await websocket.send(message)
            consumer_task = asyncio.ensure_future(self.consumer_handler(websocket, path))
            producer_task = asyncio.ensure_future(self.producer_handler(websocket, path))
            done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
        finally:
            self.connected.remove(websocket)

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consume(message)

    async def producer_handler(self, websocket, path):
        while True:
            await asyncio.sleep(1)
            message = await self.produce()
            await websocket.send(message)

    async def consume(self, message):
        command, *args = message.split()
        print(command, args)
        if command == 'play':
            self.player.play()
        elif command == 'pause':
            self.player.pause()
        elif command == 'stop':
            self.player.stop()
        elif command == 'station':
            try:
                relative, difference = parse_change(args)
                self.player.switch_station(relative * self.player.current_station_id + difference)
            except (IndexError, ValueError):
                return
        elif command == 'audiodevice':
            available = self.player.available_audio_devices
            if len(args) == 0 and '' in available.keys():
                self.player.switch_audio_device('')
            elif args[0] in available.keys():
                self.player.switch_audio_device(args[0])
        elif command == 'volume':
            try:
                relative, difference = parse_change(args)
                self.player.set_volume(relative * self.player.volume + difference)
            except (IndexError, ValueError):
                return
        elif message == 'shutdown':
            self.player.stop()
            if sys.platform.startswith('linux'):
                os.system('shutdown -h now')  # requires 'chmod 4755 /sbin/shutdown'
            elif sys.platform.startswith('win'):
                os.system('shutdown -s -t 0')
            else:
                pass  # not supported

    async def produce(self):
        return json.dumps(
            {'playing': self.player.currently_playing,
            'is_playing': self.player.is_playing,
            'station': self.player.current_station_id,
            'stations': self.player.available_stations,
            'volume': self.player.volume,
            'audiodevice': self.player.current_audio_device,
            'connections': len(self.connected),
            'audiodevices': self.player.available_audio_devices})

    def serve(self, *args, **kwargs):
        return websockets.serve(self.handler, *args, **kwargs)
