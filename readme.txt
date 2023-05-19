\*in the future i will finish the readme file, right now its just text

simple project that includes:

1. balls (nodes)
2. springs
3. soft objects (made from a group of balls)
4. hitboxes
5. custom made Vec2 class
6. strings (not finished)
7. effect areas
this project only has the basics right now + a menu to pick objects from, but both features are not complete. in the future maybe it will become a game where you need to get the green ball to the objective with minimal resources, or just a sandbox.

right now there are about 1,000 lines written.

controls (besides menu, the menu is functional besides the made up names that will crash you if you pick an undefined object): num-0 to num-5: change to mode 0 to 5

mode 0:
left-click: pick up and move balls (if you move balls outside of the frame they will get deleted)

mode 1: left-click: create ball
right-click: delete ball nearest to cursor (doesnt work on green ball)

mode 2:
left-click: select nearest ball 1
right-click: select nearest ball 2
middle-click: connect 2 selected balls with spring (string has length, force and damping. default damping is 0)

mode 3:
left-click: mark point 1
right-click: mark point 2
middle-click: create hitbox between 2 points (hit boxes are 1 sided)

mode 4:
left-click: mirror nearest hitbox
right-click: delete nearest hitbox

mode 5:
right-click: add node to list
middle-click: create polygon (soft body) from all nodes in list
left-click: remove all polygons

the settings are not safe so the program may crash if you are not careful.
the soft object simulation is quite addicting i recommend messing with it.
also, there are 2 function simulation types for the soft bodies. both work best when the mass
of all the balls in the polygon are the same.
