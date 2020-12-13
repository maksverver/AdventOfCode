import Data.List

solvePart1 :: [Int] -> Int
solvePart1 diffs = length ones * length threes
    where [ones@(1:_), threes@(3:_)] = group $ sort diffs

solvePart2 :: [Int] -> Integer
solvePart2 diffs = head $ foldl' update [1] diffs
    where
        update :: [Integer] -> Int -> [Integer]
        update counts diff | diff > 0 = sum counts':counts'
            where counts' = take 3 (replicate (diff - 1) 0 ++ counts)

main = do
    input <- getContents
    let inputInts = sort $ map read (lines input)
    let allInts = [0] ++ inputInts ++ [last inputInts + 3]
    let diffs = [y - x | (x, y) <- zip allInts (tail allInts)]
    print $ solvePart1 diffs
    print $ solvePart2 diffs
