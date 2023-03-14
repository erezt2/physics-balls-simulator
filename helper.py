import pygame as pg, math

pg.init()
pg.font.init()

WINDOW_WIDTH = 799
WINDOW_HEIGHT = 599


PI = math.pi
font = pg.font.SysFont("Aharoni", 32)


def both_ranges(x, y, z):
    return x <= y <= z or z <= y <= x


def fake_atan2(y, x):
    c = 0
    if x < 0:
        if y >= 0:
            c = 2
        else:
            c = -2
    elif x == 0:
        if y > 0:
            c = 1
        elif y == 0:
            return None
        else:
            c = -1
        return c
    return x / (1 + abs(x)) + c


def min_max(minimum, value, maximum):
    if minimum > maximum:
        return minimum
    return max(min(value, maximum), minimum)


class Vars:
    menu_click_pos = None
    menu_moved = False
    mouse_click = False
    scroll = False


if True:
    keysList = {
        "a": pg.K_a,
        "b": pg.K_b,
        "c": pg.K_c,
        "d": pg.K_d,
        "e": pg.K_e,
        "f": pg.K_f,
        "g": pg.K_g,
        "h": pg.K_h,
        "i": pg.K_i,
        "j": pg.K_j,
        "k": pg.K_k,
        "l": pg.K_l,
        "m": pg.K_m,
        "n": pg.K_n,
        "o": pg.K_o,
        "p": pg.K_p,
        "q": pg.K_q,
        "r": pg.K_r,
        "s": pg.K_s,
        "t": pg.K_t,
        "u": pg.K_u,
        "v": pg.K_v,
        "w": pg.K_w,
        "x": pg.K_x,
        "y": pg.K_y,
        "z": pg.K_z,
        "space": pg.K_SPACE,
        "1": pg.K_1,
        "2": pg.K_2,
        "3": pg.K_3,
        "4": pg.K_4,
        "5": pg.K_5,
        "6": pg.K_6,
        "7": pg.K_7,
        "8": pg.K_8,
        "9": pg.K_9,
        "0": pg.K_0,
        "num0": pg.K_KP0,
        "num1": pg.K_KP1,
        "num2": pg.K_KP2,
        "num3": pg.K_KP3,
        "num4": pg.K_KP4,
        "num5": pg.K_KP5,
        "num6": pg.K_KP6,
        "num7": pg.K_KP7,
        "num8": pg.K_KP8,
        "num9": pg.K_KP9,
        "numDel": pg.K_KP_PERIOD,
        "up": pg.K_UP,
        "right": pg.K_RIGHT,
        "down": pg.K_DOWN,
        "left": pg.K_LEFT,
        "shift": pg.K_LSHIFT,
        "ctrl": pg.K_LCTRL,
        "esc": pg.K_ESCAPE,
        "tab": pg.K_TAB,
        "+": pg.K_KP_PLUS,
        "-": pg.K_KP_MINUS,
        ":": pg.K_SEMICOLON,
        "del": pg.K_DELETE,
        "\'": pg.K_QUOTE,
        ".": pg.K_PERIOD,
        ",": pg.K_COMMA,
        "?": pg.K_SLASH,
        "_": pg.K_MINUS,
        "NP_enter": pg.K_KP_ENTER,
        "enter": pg.K_RETURN,
        "\b": pg.K_BACKSPACE,
    }
    mouseDown = {key+1: False for key in range(7)}
    keysDown = {key: False for key in keysList}
    mouseHeld = {key+1: False for key in range(7)}
    keysHeld = {key: False for key in keysList}
    mouseUp = {key+1: False for key in range(7)}
    keysUp = {key: False for key in keysList}


def draw_text(window, text, pos, width=0):

    temp_text = ""
    res = []
    pre = ""
    first = True
    for i in text.split(" "):
        w = font.render(temp_text + pre + i, False, (255, 255, 255)).get_width()
        if first and w > width:
            res.append(i)
            continue
        first = False
        if width == 0 or w <= width:
            temp_text += pre + i
        else:
            res.append(temp_text)
            temp_text = i
        pre = " "
    res.append(temp_text)

    line = 0
    for i in res:
        surface = font.render(i, False, (255, 255, 255))
        window.blit(surface, (pos[0], pos[1] + line))
        line += 32

    return line


def key_list():
    Vars.mouse_click = False

    if True:
        for reset_key in mouseDown:
            mouseDown[reset_key] = False
        for reset_key in mouseUp:
            mouseUp[reset_key] = False
        for reset_key in keysDown:
            keysDown[reset_key] = False
        for reset_key in keysUp:
            keysUp[reset_key] = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True

        if event.type == pg.MOUSEBUTTONDOWN:
            mouseDown[event.button] = True
            mouseHeld[event.button] = True

        if event.type == pg.MOUSEBUTTONUP:
            mouseUp[event.button] = True
            mouseHeld[event.button] = False

        if event.type == pg.KEYDOWN:
            for key in keysList:
                if event.key == keysList[key]:
                    keysDown[key] = True
                    keysHeld[key] = True

        if event.type == pg.KEYUP:
            for key in keysList:
                if event.key == keysList[key]:
                    keysUp[key] = True
                    keysHeld[key] = False

    return False