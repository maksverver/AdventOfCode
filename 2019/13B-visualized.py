from intcode import RunInteractive
from time import sleep
import curses

with open('testdata/13.in') as f:
    ints = list(map(int, f.readline().split(',')))
ints[0] = 2

x = y = None
paddle_x = ball_x = None

def Input():
    game_win.refresh()
    score_win.refresh()
    sleep(0.1)
    return (paddle_x < ball_x) - (paddle_x > ball_x)

def Output(i):
    global x, y, paddle_x, ball_x
    if x is None:
        x = i
    elif y is None:
        y = i
    else:
        if x >= 0 and y >= 0:
            assert x < 37 and y < 23
            game_win.addch(y, x, ".#$=o"[i])
            if i == 3:
                paddle_x = x
            if i == 4:
                ball_x = x
        else:
            assert x == -1 and y == 0
            score_win.addstr(0, 0, "Score: %d" % i)
        x = y = None

stdscr = curses.initscr()

score_win = curses.newwin(1, 38, 0, 0)
game_win = curses.newwin(23, 38, 1, 0)
stdscr.refresh()

RunInteractive(ints, Input, Output)
