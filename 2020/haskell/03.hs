rotate :: Int -> [a] -> [a]
rotate n xs = drop n xs ++ take n xs

solve :: Int -> Int -> [String] -> Int
solve right down grid = solve' grid
    where
        solve' [] = 0
        solve' grid = a + b
            where
                a = fromEnum (head (head grid) == '#')
                b = solve' (map (rotate right) (drop down grid))

main = do
    input <- getContents
    let grid = lines input
    print $ solve 3 1 grid
    print $ product [solve right down grid | (right, down) <- slopes]
    where slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
