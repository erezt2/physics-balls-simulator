from vec2 import Vec2
from body import Body
from node import Node
from hitbox import Hitbox
from spring import Branch
from window import Win
from polygon import Polygon
from string import Tail
from objective import Area
from helper import *

import pygame as pg, time, random, pickle, os
import math


# click lists


class Func:
    @classmethod
    def none(cls, area, node):
        pass

    @classmethod
    def quit(cls, area, node):
        return
        if Body.ins.main_node is node:
            print("yeet")


func_list = {
    "none": Func.none,
    "quit": Func.quit,
}


def key_handle(body, mouse_pos, rt):
    if keysDown["s"]:
        _f = open(f"levels original/{Win.save_name}.txt", "wb")
        pickle.dump(body, _f)
        _f.close()
    if mouseDown[4]:
        Win.menu_scroll -= 12
    if mouseDown[5]:
        Win.menu_scroll += 12
    if keysDown["enter"]:
        Win.simulate = not Win.simulate
    if keysDown["up"]:
        Win.simulate_once = True

    def reset_rt(_rt):
        _rt.mode1 = None
        _rt.mode2 = None
        _rt.polygon.clear()

    if keysDown["num0"]:
        rt.mode = "none"
        reset_rt(rt)
    if keysDown["num1"]:
        rt.mode = "node"
        reset_rt(rt)
    if keysDown["num2"]:
        rt.mode = "branch"
        reset_rt(rt)
    if keysDown["num3"]:
        rt.mode = "hitbox"
        reset_rt(rt)
    if keysDown["num4"]:
        rt.mode = "hitboxedit"
        reset_rt(rt)
    if keysDown["num5"]:
        rt.mode = "polygon"
        reset_rt(rt)
    if mouseDown[1]:
        if Win.width + 244 > mouse_pos.x > Win.width:
            Vars.menu_click_pos = Vec2(mouse_pos)
            Vars.menu_moved = False
        if mouse_pos.x > Win.width + 244:
            Vars.scroll = True
        # mode settings
        if mouse_pos.x < Win.width:
            if Win.selected_item is not None:
                item = Body.components[Win.selected_item]
                _type = item[0].lower()
                args = item[1:]
                if _type == "node":
                    body.nodes.append(Node(body, mouse_pos, *args))
                elif _type == "branch":
                    pass
                elif _type == "area":
                    size = Vec2(args[0])
                    body.areas.append(Area(mouse_pos - size / 2, size, *args[1:]))
                elif _type == "hitbox":
                    pass

            if rt.mode == "none":
                temp = body.nodes[body.choose_nearest_node(mouse_pos - Win.camera)]
                if (temp.pos - mouse_pos - Win.camera).length2() < temp.radius ** 2:
                    rt.mode1 = temp
            elif rt.mode == "node":
                temp = Node(body, mouse_pos - Win.camera)
                body.nodes.append(temp)
            elif rt.mode == "branch":
                rt.mode1 = body.choose_nearest_node(mouse_pos - Win.camera)
            elif rt.mode == "hitbox":
                rt.mode1 = mouse_pos - Win.camera
            elif rt.mode == "hitboxedit":
                temp = body.choose_nearest_hitbox(mouse_pos - Win.camera)
                body.hitboxes[temp].normal *= -1
            elif rt.mode == "polygon":
                temp = body.choose_nearest_node(mouse_pos - Win.camera)
                rt.polygon.append(temp)
    if mouseDown[2]:
        if rt.mode == "branch":
            body.branches.append(Branch(body.nodes[rt.mode1], body.nodes[rt.mode2], 30))
        elif rt.mode == "hitbox":
            body.hitboxes.append(Hitbox(rt.mode1, rt.mode2))
        # elif rt.mode == "hitboxedit":
        #     body.hitboxes.append(Hitbox(rt.mode1, rt.mode2))
        elif rt.mode == "polygon":
            body.polygons.append(Polygon(body, rt.polygon))
            rt.polygon.clear()
    if mouseDown[3]:
        if Win.selected_item is not None:
            body.toolbox.append(Win.selected_item)
            Win.selected_item = None
        if rt.mode == "none":
            rt.mode1 = None
        elif rt.mode == "node":
            temp = body.choose_nearest_node(mouse_pos - Win.camera)
            if temp != 0:
                body.remove_node(temp)

        elif rt.mode == "branch":
            rt.mode2 = body.choose_nearest_node(mouse_pos - Win.camera)
        elif rt.mode == "hitbox":
            rt.mode2 = mouse_pos - Win.camera
        elif rt.mode == "hitboxedit":
            temp = body.choose_nearest_hitbox(mouse_pos - Win.camera)
            body.remove_hitbox(temp)
        elif rt.mode == "polygon":
            body.polygons.clear()
        # elif rt.mode == "polygon":
        #     nodes = [body.nodes[node] for node in rt.polygon]
        #     temp = body.choose_nearest_node(mouse_pos - Win.camera, nodes)
        #     rt.polygon.remove(temp)
    if mouseUp[1]:
        Vars.menu_click_pos = None
        Vars.scroll = False
        if not Vars.menu_moved:
            if mouse_pos.x > Win.width:
                Vars.mouse_click = True
        if rt.mode == "none":
            rt.mode1 = None
    if mouseHeld[1]:
        if Vars.menu_click_pos is not None and (mouse_pos - Vars.menu_click_pos).length2() > 3**2:
            Vars.menu_moved = True
        if Vars.menu_click_pos is not None:
            Win.menu_scroll += mouse_pos.y - Vars.menu_click_pos.y
            Vars.menu_click_pos = mouse_pos
        if Vars.scroll:
            Win.menu_scroll = (Win.height - mouse_pos.y - rt.section / 2) / (Win.height - rt.section) * (rt.total - Win.height)
            Win.menu_scroll = min_max(0, Win.menu_scroll, rt.total - Win.height)


def simulate(body, rt):
    if Win.simulate or Win.simulate_once:
        for node in body.nodes:
            node.forces = node.apply_force([])

        for node in body.nodes:
            for area in body.areas:
                area.calculate_frame(node, func_list)

        temp = list(body.branches)
        if Win.randomize:
            random.shuffle(temp)
        for branch in temp:
            branch.apply_node_forces()
        for polygon in body.polygons:
            polygon.apply_forces()

        temp = list(body.nodes)
        if Win.randomize:
            random.shuffle(temp)
        for node in temp:
            if rt.mode == "none" and rt.mode1 == node:
                continue
            node.calculate_frame(Win.fps)


def calc_camera(body, rt):
    pos = Vec2(body.main_node.pos)
    pos.x = min_max(Win.width // 2, pos.x, body.width + (-Win.width) // 2)
    pos.y = min_max(Win.height // 2, pos.y, body.height + (-Win.height) // 2)
    Win.camera = Vec2(Win.width // 2, Win.height // 2) - pos


def draw(body, mouse_pos, rt):
    for area in body.areas:
        area.draw(Win.win, Win.camera)

    for branch in body.branches:
        branch.draw(Win.win, Win.camera)

    for hitbox in body.hitboxes:
        hitbox.draw(Win.win, Win.camera)
        if Win.debug:
            hitbox.draw_normal()

    for node in body.nodes:
        node.draw(Win.win, Win.camera)

    # settings draw
    if rt.mode == "branch":
        if rt.mode1 is not None:
            pg.draw.circle(Win.win, (255, 255, 255), body.nodes[rt.mode1].pos.fit(Win.camera), body.nodes[rt.mode1].radius + 3, 2)
        if rt.mode2 is not None:
            pg.draw.circle(Win.win, (255, 255, 255), body.nodes[rt.mode2].pos.fit(Win.camera), body.nodes[rt.mode2].radius + 3, 2)

    if rt.mode == "polygon":
        for node in rt.polygon:
            pg.draw.circle(Win.win, (255, 255, 255), body.nodes[node].pos.fit(Win.camera), body.nodes[node].radius + 3, 2)

    elif rt.mode == "hitbox":
        if rt.mode1 is not None:
            pg.draw.circle(Win.win, (255, 255, 255), rt.mode1.fit(Win.camera), 3, 2)
        if rt.mode2 is not None:
            pg.draw.circle(Win.win, (255, 255, 255), rt.mode2.fit(Win.camera), 3, 2)

    elif rt.mode == "none":
        if rt.mode1 is not None:
            rt.mode1.pos = mouse_pos
            rt.mode1.vel = Vec2()


def draw_menu(body, mouse_pos, rt):
    pg.draw.rect(Win.win, (100, 100, 100), (Win.width + 1, 0, 250, Win.height + 1))
    i = 3 - Win.menu_scroll
    pos = 0
    for obj in body.toolbox:
        h = draw_text(Win.win, obj, (Win.width + 10, i + 4), 235)
        pg.draw.rect(Win.win, (255, 255, 255), (Win.width + 3, i, 240, h + 6), 1)
        if Vars.mouse_click and Win.width + 3 < mouse_pos.x < Win.width + 243 and i < mouse_pos.mirror().y < i + h + 6:
            if Win.selected_item is None:
                Win.selected_item = body.toolbox[pos]
                body.toolbox.pop(pos)
            else:
                body.toolbox.insert(pos + 1, Win.selected_item)
                Win.selected_item = body.toolbox[pos]
                body.toolbox.pop(pos)
        i += 16 + h
        pos += 1

    rt.total = i + Win.menu_scroll - 8
    Win.menu_scroll = min_max(0, Win.menu_scroll, rt.total - Win.height)
    rt.section = Win.height ** 2 / rt.total
    rt.section2 = Win.menu_scroll / (rt.total - Win.height) * (Win.height - rt.section - 4)
    pg.draw.rect(Win.win, (255, 255, 255), (Win.width + 245, rt.section2 + 3, 3, rt.section))


def main():
    body = Body(Vec2(799, 599))

    class Runtime:
        mode = "none"
        mode1 = None
        mode2 = None
        polygon = []
        total = 0
        section = 0
        section2 = 0

    rt = Runtime()

    # a = 300
    # for i in range(20):
    #     Tail(3, i // 2, Vec2(0, 2*i + 5))
    # for i in range(a - 20):
    #     Tail(3, a // 30 - i // 30 + 1, Vec2(0, 2*i + 5))

    # for i in range(a):
        # Tail(80, 4, Vec2(0, 2 * i + 5))

    while Win.run:
        # time handle
        if time.time() - Win.last_frame < Win.slow_mo / Win.fps:
            continue
        Win.last_frame = time.time()

        # mouse pos
        mouse_pos = Vec2(pg.mouse.get_pos())
        mouse_pos = Vec2(mouse_pos[0], Win.height - mouse_pos[1])

        # frame beginning handle
        Win.win.fill(body.bg_color)
        Win.simulate_once = False
        if key_list():
            Win.run = False
            continue

        # key handle
        key_handle(body, mouse_pos, rt)
        simulate(body, rt)
        # camera calc
        calc_camera(body, rt)
        # draw body
        draw(body, mouse_pos, rt)

        # draw flip camera
        Win.win.blit(pg.transform.flip(Win.win, False, True), (0, 0))
        # draw menu
        draw_menu(body, mouse_pos, rt)
        ##########
        # misc
        for i in body.nodes:
            if not (both_ranges(-10, i.pos.x, Win.width + 10) and both_ranges(-10, i.pos.y, Win.height + 10)):
                print("NODE ESCAPED !!!!")
                body.nodes.remove(i)
        # calculate destination
        """
        Body.ins.main_node.pos.mirror()
        mouse_pos.mirror()
        """
        ## tail
        # Tail.tail_list[0].follow(mouse_pos.mirror())
        # for i in range(a-1):
        #     Tail.tail_list[i+1].follow(Tail.tail_list[i].pos)
        #
        # # follow base point (not required)
        # # Tail.tail_list[-1].pos = Vec2()
        # # for i in range(a-2, -1, -1):
        # #     Tail.tail_list[i].pos = Tail.tail_list[i+1].pos + Tail.tail_list[i+1].par * Tail.tail_list[i+1].len
        #
        # # draw
        # for i in range(a):
        #     Tail.tail_list[i].draw(Win.win, Win.camera)
        # ##
        #
        # # text for selected item
        if Win.selected_item is not None:
            surface = font.render(Win.selected_item, False, (255, 255, 255))
            Win.win.blit(surface, (5, 3))

        pg.display.flip()


if __name__ == "__main__":
    main()

pg.quit()
quit()
