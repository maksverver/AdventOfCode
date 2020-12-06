-- `find len sum nums` returns all subsequences of `nums` with length `len` and sum `sum`.
find :: Int -> Int -> [Int] -> [[Int]]
find 0   0   _          = [[]]
find 0   _   _          = []
find _   _   []         = []
find len sum (num:nums) = find len sum nums ++ map (num:) (find (len - 1) (sum - num) nums)

main = do
    input <- getContents
    let nums = map read (lines input) :: [Int]
    let [pair] = find 2 2020 nums
    print $ product pair
    let [triple] = find 3 2020 nums
    print $ product triple
