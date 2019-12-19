from intcode import ReadInts, RunInteractive

ints = ReadInts()
ints[0] = 2

x = y = None
paddle_x = ball_x = score = None

def Input():
    return (paddle_x < ball_x) - (paddle_x > ball_x)

def Output(i):
    global x, y, paddle_x, ball_x, score
    if x is None:
        x = i
    elif y is None:
        y = i
    else:
        if x >= 0 and y >= 0:
            if i == 3:
                paddle_x = x
            if i == 4:
                ball_x = x
        else:
            assert x == -1 and y == 0
            score = i
        x = y = None

RunInteractive(ints, Input, Output)
print(score)
