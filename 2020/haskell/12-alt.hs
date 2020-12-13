import Data.List

type Ship = (Int, Int, Int, Int)
data Command = Move Int Int | Turn Int | Forward Int

moveShip x y (sx, sy, dx, dy) = (sx + x, sy + y, dx, dy)

moveWaypoint x y (sx, sy, dx, dy) = (sx, sy, dx + x, dy + y)

turn angle (sx, sy, dx, dy) = (sx, sy, dx', dy')
    where
        (dx', dy') = case angle of
            90  -> (-dy,  dx)
            180 -> (-dx, -dy)
            270 -> ( dy, -dx)

forward n (sx, sy, dx, dy) = (sx + dx*n, sy + dy*n, dx, dy)

apply1 :: Command -> Ship -> Ship
apply1 (Move x y)  = moveShip x y
apply1 (Turn a)    = turn a
apply1 (Forward n) = forward n

apply2 :: Command -> Ship -> Ship
apply2 (Move x y)  = moveWaypoint x y
apply2 (Turn a)    = turn a
apply2 (Forward n) = forward n

dist :: Ship -> Int
dist (sx, sy, _, _) = abs sx + abs sy

main = do
    input <- getContents
    let commands = map parse $ lines input
    let solve apply initial = dist $ foldl' (flip apply) initial commands
    print $ solve apply1 (0, 0,  1, 0)
    print $ solve apply2 (0, 0, 10, 1)
    where
        parse (c:s) = case c of
            'N' -> Move 0 i
            'E' -> Move i 0
            'S' -> Move 0 (-i)
            'W' -> Move (-i) 0
            'L' -> Turn i
            'R' -> Turn (360 - i)
            'F' -> Forward i
            where i = read s :: Int
