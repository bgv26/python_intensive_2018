import math
import random
import turtle

window = turtle.Screen()
window.setup(1200, 800)
window.bgpic("images/background.png")

BASE_X, BASE_Y = 0, -300
ENEMY_Y = 400


def calc_heading(from_x, from_y, to_x, to_y):
    delta_x = to_x - from_x
    delta_y = to_y - from_y
    length = (delta_x ** 2 + delta_y ** 2) ** 0.5
    alpha = math.degrees(math.acos(delta_x / length))
    if delta_y < 0:
        alpha = -alpha
    return alpha


def fire_missile(from_x, from_y, to_x, to_y, color, owner):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=from_x, y=from_y)
    missile.pendown()
    heading = calc_heading(from_x=from_x, from_y=from_y, to_x=to_x, to_y=to_y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': (to_x, to_y),
            'state': 'launched', 'radius': 0}
    owner.append(info)


def fire_our_missile(x, y):
    fire_missile(BASE_X, BASE_Y, x, y, 'white', our_missiles)


def fire_enemy_missile():
    fire_missile(random.randint(-600, 600), ENEMY_Y, BASE_X, BASE_Y, 'red', enemy_missiles)


def turn(owner):
    for info in owner:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(target) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info['radius'])

    dead_missiles = [info for info in owner if info['state'] == 'dead']
    for dead in dead_missiles:
        owner.remove(dead)


window.onclick(fire_our_missile)

our_missiles = []
enemy_missiles = []

for _ in range(random.randint(1, 20)):
    fire_enemy_missile()

while True:
    window.update()

    turn(our_missiles)
    turn(enemy_missiles)
