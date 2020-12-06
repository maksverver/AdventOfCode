import Data.List (sort)
import Data.List.Split (splitOn)

union xs [] = xs
union [] ys = ys
union (x:xs) (y:ys)
    | x < y = x:union xs (y:ys)
    | x > y = y:union (x:xs) ys
    | otherwise = x:union xs ys

intersection xs [] = []
intersection [] ys = []
intersection (x:xs) (y:ys)
    | x < y = intersection xs (y:ys)
    | x > y = intersection (x:xs) ys
    | otherwise = x:intersection xs ys

main = do
    input <- getContents
    let answers = map (map sort . words) (splitOn "\n\n" input)
    print $ sum $ map (length . foldr1 union) answers
    print $ sum $ map (length . foldr1 intersection) answers
