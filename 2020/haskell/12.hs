import Data.List

type Ship = (Int, Int, Int, Int)

apply1 :: Ship -> (Char, Int) -> Ship
apply1 (sx, sy, dx, dy) (c, i) = case c of
    'N' -> (sx, sy + i, dx, dy)
    'E' -> (sx + i, sy, dx, dy)
    'S' -> (sx, sy - i, dx, dy)
    'W' -> (sx - i, sy, dx, dy)
    'L' -> (sx, sy, dx', dy') where (dx', dy') = turn i (dx, dy)
    'R' -> (sx, sy, dx', dy') where (dx', dy') = turn (360 - i) (dx, dy)
    'F' -> (sx + dx*i, sy + dy*i, dx, dy)
    where
        turn  90 (dx, dy) = (-dy,  dx)
        turn 180 (dx, dy) = (-dx, -dy)
        turn 270 (dx, dy) = ( dy, -dx)

apply2 :: Ship -> (Char, Int) -> Ship
apply2 ship@(sx, sy, dx, dy) command@(c, i) = case c of
    'N' -> (sx, sy, dx, dy + i)
    'E' -> (sx, sy, dx + i, dy)
    'S' -> (sx, sy, dx, dy - i)
    'W' -> (sx, sy, dx - i, dy)
    _ -> apply1 ship command

dist :: Ship -> Int
dist (sx, sy, _, _) = abs sx + abs sy

main = do
    input <- getContents
    let commands = map parse $ lines input
    print $ dist $ foldl' apply1 (0, 0,  1, 0) commands
    print $ dist $ foldl' apply2 (0, 0, 10, 1) commands
    where parse (c:i) = (c, read i) :: (Char, Int)
