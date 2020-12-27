import Prelude hiding (log)

mul :: Int -> Int -> Int
mul x y = x * y `mod` 20201227

log :: Int -> Int -> Int
log s y = go 0 1 where go n x = if x == y then n else go (n + 1) (mul x s)

pow :: Int -> Int -> Int
pow _ 0 = 1
pow s 1 = s
pow s n = mul (pow s (n `mod` 2)) (pow (mul s s) (n `div` 2))

main = do
    input <- getContents
    let [a, b] = map read $ lines input :: [Int]
    print $ pow a (log 7 b)
