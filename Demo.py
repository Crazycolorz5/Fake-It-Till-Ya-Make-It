# coding=utf-8
# from __future__ import print_function
from watson_developer_cloud import DiscoveryV1
import json

name = input("Welcome to Washington Elementary! Please input your name: \n>>")

print("Nice to meet you, %s. \nGood luck as your first day as a substitute teacher!\n" % name)

print("You enter the room of your history class. There are students eagerly awaiting your teaching.\n")

input("Type help for possible commands, or feel free to get started!\n>>")

# Player types help

input("room contents: Looks around the room and tells you possible interactable objects\n" + 
    "help: gives a brief description of basic commands user can enter \n" +
    "move x: moves focus of subsitute teacher to content x\n>>")

# Player types room contents

input("You find yourself in a 7th grade history classroom. \n" +
"There is a student with her hand raised, awaiting your help\n" + 
"There is the teacher's desk, the surface clean, but there is a drawer as well\n>>")

# Player types talk to student

input("The student asks you: \"So, before class starts, what date exactly\n" +
"did the War of 1812 end?\n>>")

#We don't know, so we ask Watson
#query War of 1812 
input("No information found.\n>>")

# The treaty was unanimously ratified by the United States on February 17, 1815, ending the war with Status quo ante bellum (no boundary changes).
