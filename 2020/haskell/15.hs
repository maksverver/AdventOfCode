import Data.IntMap.Strict (IntMap, (!?))
import qualified Data.IntMap.Strict as IntMap
import Data.List.Split

solve :: [Int] -> Int -> Int
solve nums target = find (v, i, index)
    where
        nums' = zip nums [1..]
        (v, i) = last nums'
        index = IntMap.fromList (init nums')
        rest = [v | (v, _, _) <- iterate next (v, i, index)]

        find (v, i, index)
            | i < target  = find $ next (v, i, index)
            | i == target = v

        next :: (Int, Int, IntMap Int) -> (Int, Int, IntMap Int)
        next (v, i, index) = (v', i + 1, IntMap.insert v i index)
            where
                v' = i - IntMap.findWithDefault i v index

main = do
    input <- getContents
    let nums = map read $ splitOn "," input
    print $ solve nums 2020
    print $ solve nums 30000000
