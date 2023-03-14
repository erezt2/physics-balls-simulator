from vec2 import *
from helper import *
import pygame as pg
import time, os, pickle


class Win:
    width = WINDOW_WIDTH
    height = WINDOW_HEIGHT

    win = pg.display.set_mode((width + 1 + 250, height + 1))
    last_frame = time.time()

    run = True

    simulate = False
    simulate_once = False
    fps = 120
    slow_mo = 1
    randomize = True

    camera = Vec2()
    menu_scroll = 0
    selected_item = None

    debug = False
    save_name = "level1"

    @classmethod
    def load_level(cls, name):
        path = f"levels/{name}.txt"
        if os.path.exists(path):
            _f = open(path, "rb")
            body = pickle.load(_f)
        else:
            _f = open(path, "wb")
            _f1 = open(f"levels original/{name}.txt", "rb")
            _f.write(_f1.read())
            body = pickle.load(_f1)
            _f1.close()
        _f.close()
        return body