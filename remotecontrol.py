#!/usr/bin/env python3

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
            message = await self.produce()
            await websocket.send(message)

    async def consume(self, message):
        if message == 'next':
            self.player.next_station()
        elif message == 'play':
            self.player.play()
        elif message == 'pause':
            self.player.pause()
        elif message == 'vol+':
            self.player.volume_inc()
        elif message == 'vol-':
            self.player.volume_dec()

    async def produce(self):
        await asyncio.sleep(1)
        return json.dumps({'playing': self.player.is_playing(), 'station': self.player.current_station_name, 'volume': self.player.volume})

    def run_forever(self):
        try:
            start_server = websockets.serve(self.handler, "localhost", 6789)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
        finally:
            self.player.stop()
