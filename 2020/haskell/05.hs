import Data.List

seatId :: String -> Int
seatId s = 8*r + c
    where
        (r, c, 1, 1) = foldl' update (0, 0, 128, 8) s

        update (r, c, h, w) 'F' = (r,      c,      h', w ) where h' = h `div` 2
        update (r, c, h, w) 'B' = (r + h', c,      h', w ) where h' = h `div` 2
        update (r, c, h, w) 'L' = (r,      c,      h,  w') where w' = w `div` 2
        update (r, c, h, w) 'R' = (r,      c + w', h,  w') where w' = w `div` 2

findMissing :: [Int] -> [Int]
findMissing [_] = []
findMissing (x:y:ys) = [x + 1..y - 1] ++ findMissing (y:ys)

main = do
    input <- getContents
    let seatIds = map seatId (lines input)
    print $ maximum seatIds
    let [missingSeatId] = findMissing (sort seatIds)
    print missingSeatId

