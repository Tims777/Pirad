#!/usr/bin/env python3

import os
import sys
import asyncio
import json
import websockets


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
        if message == 'next':
            self.player.next_station()
        elif message == 'play':
            self.player.play()
        elif message == 'pause':
            self.player.pause()
        elif message == 'stop':
            self.player.stop()
        elif message == 'vol+':
            self.player.volume_inc()
        elif message == 'vol-':
            self.player.volume_dec()
        elif message == 'shutdown':
            self.player.stop()
            if sys.platform.startswith('linux'):
                os.system('shutdown -r now')  # requires 'chmod 4755 /sbin/shutdown'
            elif sys.platform.startswith('win'):
                os.system('shutdown -s -t 0')
            else:
                pass  # not supported

    async def produce(self):
        return json.dumps({'playing': self.player.is_playing(), 'station': self.player.current_station_name, 'volume': self.player.volume, 'connections': len(self.connected)})

    def serve(self, *args, **kwargs):
        return websockets.serve(self.handler, *args, **kwargs)
