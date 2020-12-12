import qualified Data.IntSet as IntSet
import Data.List
import Queue

-- Naive implementation which takes time O(N^2)
--hasPairWithSum :: [Int] -> Int -> Bool
--hasPairWithSum nums sum = pairs /= []
--    where pairs = [(a, b) | (a:rest) <- tails nums, b <- rest, a + b == sum]

-- Optimized implementation which takes time O(N*W) where W is the size of Int.
-- Note: this assumes `nums` are distinct, which isn't explicitly stated but
-- appears to be true.
hasPairWithSum :: [Int] -> Int -> Bool
hasPairWithSum nums sum = find IntSet.empty nums
    where
        find _    []     = False
        find seen (x:xs) = IntSet.member (sum - x) seen || find (IntSet.insert x seen) xs

solvePart1 :: [Int] -> Int
solvePart1 nums = head $ head $ filter (not . valid) lists
    where
        -- List of reversed prefixes of `nums` of length at least 26.
        lists = drop 26 $ reverse $ tails $ reverse nums

        -- A prefix is valid if the last element is the sum of a pair of the 25
        -- previous elements.
        valid (x:xs) = hasPairWithSum (take 25 xs) x

solvePart2 :: [Int] -> Int -> [Int]
solvePart2 nums target = toList $ solve nums (fromList []) 0 
    where
        solve :: [Int] -> Queue Int -> Int -> Queue Int
        solve nums kept total 
            | total < target = let (x:xs) = nums in solve xs (push kept x) (total + x)
            | total > target = let (x, kept') = pop kept in solve nums kept' (total - x)
            | otherwise      = kept

main = do
    input <- getContents
    let nums = map read (lines input) :: [Int]
    let answer1 = solvePart1 nums
    let sublist = solvePart2 nums answer1
    let answer2 = minimum sublist + maximum sublist
    print answer1
    print answer2
