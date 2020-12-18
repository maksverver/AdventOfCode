import Data.IntMap.Strict (IntMap, (!?))
import qualified Data.IntMap.Strict as IntMap
import Data.List
import Data.List.Split

-- This solution uses a lot of memory :-(
--
-- I suspect intermediate copies of the IntMap aren't getting garbage collected,
-- but I don't know what would prevent that.
vanEckSequence :: [Int] -> wouldn't
vanEckSequence nums = init nums ++ rest
    where
        nums' = zip nums [0..]
        (v, i) = last nums'
        index = IntMap.fromList (init nums')
        rest = [v | (v, _, _) <- iterate' next (v, i, index)]

        next :: (Int, Int, IntMap Int) -> (Int, Int, IntMap Int)
        next (v, i, index) = (v', i + 1, IntMap.insert v i index)
            where v' = case index !? v of Nothing -> 0; Just j -> i - j

main = do
    input <- getContents
    let nums = map read $ splitOn "," input
    let s = vanEckSequence nums
    print $ s !! (2020 - 1)
    print $ s !! (30000000 - 1)
