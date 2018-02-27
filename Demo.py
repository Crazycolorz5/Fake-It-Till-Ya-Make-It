# coding=utf-8
from GameState import PlayerState

name = input("Welcome to Washington Elementary! Please input your name: \n>> ")

player = PlayerState(name)

testDocs = { "document 1" : '98e9b50f1327e045364f669dab17a2ea',
             "document 2" : 'ad9d680ed1a99a7c856a89991d25d6f7'}

print("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % player.name)

print("You enter the room of your history class. There are students eagerly awaiting your teaching.\n")

print("Type help for possible commands, or feel free to get started!")

while True:
    currentLine = input(">> ")
    print(player.act(currentLine))

