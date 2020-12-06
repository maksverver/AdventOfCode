import Data.List
import Data.List.Split

main = do
    input <- getContents
    let answers = map words(splitOn "\n\n" input)
    print $ sum $ map (length . foldr1 union) answers
    print $ sum $ map (length . foldr1 intersect) answers
