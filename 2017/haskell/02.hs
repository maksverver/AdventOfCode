import System.IO.Unsafe

readInput :: IO [[Int]]
readInput = map (map read . words) . lines <$> getContents

rowsum1 :: [Int] -> Int
rowsum1 row = maximum row - minimum row

rowsum2 :: [Int] -> Int
rowsum2 row = only [div x y | x <- row, y <- row, x > y, mod x y == 0]
    where only [x] = x
          only _ = error "Ambiguous input!"

checksum :: ([Int] -> Int) -> [[Int]] -> Int
checksum rowsum = sum . map rowsum

main = do
    input <- readInput
    print $ checksum rowsum1 input
    print $ checksum rowsum2 input
