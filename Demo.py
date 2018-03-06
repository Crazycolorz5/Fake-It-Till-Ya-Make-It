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
  def out(self, string): print(self, string)
  inp = lambda self, prompt: input(prompt)

class WebsocketHandler(IOHandler):
  def __init__(self, websocket):
    self.websocket = websocket
  def out(self, string):
    await self.websocket.send(string)
  def inp(self, string):
    self.out(string)
    return await ws.recv()

if "--websocket" in argv:
  loop = asyncio.get_event_loop()
  asyncio.ensure_future(websockets.serve(websocketHandler, 'localhost', 10000))
else:
  gameLoop(Console())

def websocketHandler(websocket, path):
  gameLoop(WebsocketHandler(websocket))

def gameLoop(handler):
  try:
    name = handler.inp("Welcome to Washington Elementary! Please input your name: \n>> ")
    handler.out("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % player.name)
    handler.out("You enter the room of your history class. There are students eagerly awaiting your teaching.\n")
    handler.out("Type help for possible commands, or feel free to get started!")
    player = PlayerState(name)
    while True:
      currentLine = handler.inp(">> ")
      handler.out(player.act(currentLine))
  except websockets.exceptions.ConnectionClosed as e:
      quit()

    
print("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % player.name)

      
_thread.start_new_thread(gameLoop, ())