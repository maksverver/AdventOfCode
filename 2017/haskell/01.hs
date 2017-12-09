import Data.Char (digitToInt)

rotate n list = drop n list ++ take n list

evaluate x y
    | x == y    = x
    | otherwise = 0

solve :: Int -> [Int] -> Int
solve n list = sum $ zipWith evaluate list (rotate n list)

main = do
    digits <- map digitToInt <$> getLine
    print $ solve 1 digits
    let n = div (length digits) 2
    print $ solve n digits
