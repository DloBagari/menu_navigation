#!/usr/bin/python2.7
from draw_menu import DrawMenu
import curses
import json


with DrawMenu("file.json") as sk:
    sk.navigate()
