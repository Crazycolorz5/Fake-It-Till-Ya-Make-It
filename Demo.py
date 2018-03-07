# coding=utf-8
from Discovery import *
import websockets
import asyncio
import _thread
from GameState import PlayerState
from sys import argv

class IOHandler:
    def out(string):
        raise NotImplementedError()
    def inp(string):
        raise NotImplementedError()
        
class Console(IOHandler):
    async def out(self, string): 
        print(string)
    async def inp(self, prompt): 
        return input(prompt)
    def multiInstance(self):
        return False

class WebsocketHandler(IOHandler):
    def __init__(self, websocket):
        self.websocket = websocket
    async def out(self, string):
        await self.websocket.send(string)
    async def inp(self, string):
        await self.out(string)
        return await self.websocket.recv()
    def multiInstance(self):
        return True

async def websocketHandler(websocket, path):
    print('new connection')
    await gameLoop(WebsocketHandler(websocket))
    print('websocket closed')
    websocket.close()


async def gameLoop(handler):
    try:
        name = await handler.inp("Welcome to Washington Elementary! Please input your name: \n>> ")
        player = PlayerState(name)
        await handler.out("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % player.name)
        await handler.out("You enter the room of your history class. There are students eagerly awaiting your teaching.\n")
        await handler.out("Type help for possible commands, or feel free to get started!")

        while True:
            currentLine = await handler.inp(">> ")
            if "quit" == currentLine:
                if handler.multiInstance():
                    return
                else:
                    quit()

            await handler.out(player.act(currentLine))

    except websockets.exceptions.ConnectionClosed as e:
        return


if "--websocket" in argv:
    handler = websockets.serve(websocketHandler, None, 10000)
    print('websocket running')
else:
    handler = asyncio.ensure_future(gameLoop(Console()))

loop = asyncio.get_event_loop()
asyncio.ensure_future(handler)
_thread.start_new_thread(loop.run_forever())
