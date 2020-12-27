import Data.List (sort)
import Data.List.Split (splitOn)
import SortedList

main = do
    input <- getContents
    let answers = map (map sort . words) (splitOn "\n\n" input)
    print $ sum $ map (length . foldr1 union) answers
    print $ sum $ map (length . foldr1 intersection) answers
