import Data.Array
import Data.List
import Data.Maybe

enumerate :: [a] -> [(Int, a)]
enumerate = zip [0..]

-- Given a 2D array of characters, returns a list of the (row, column)
-- pairs of the `target` characters.
findCoords :: Char -> [[Char]] -> [(Int, Int)]
findCoords target grid = [(row, col) | (row, line) <- enumerate grid, (col, ch) <- enumerate line, ch == target]

-- Converts a list of seat coordinates to a list of adjacency lists.
--
-- The result has the same length as `coord`. The element at index `i` contains
-- all indices `j` adjacent to `i`.
--
-- `dists` is a list of distances that should be considered when calculating
-- distance in each of the 8 possible direction.
getAdjacencyLists :: [Int] -> [(Int, Int)] ->  [[Int]]
getAdjacencyLists dists coords
    = map (mapMaybe findSeat . rays) coords
    where
        bounds = ((0, 0), (max_row, max_col)) :: ((Int, Int), (Int, Int))
            where
                max_row = maximum (map fst coords)
                max_col = maximum (map snd coords)

        seatIndex :: Array (Int, Int) (Maybe Int)
        seatIndex = listArray bounds (repeat Nothing) // [(rc, Just i) | (i, rc) <- enumerate coords]

        findSeat :: [(Int, Int)] -> Maybe Int
        findSeat rcs = listToMaybe $ mapMaybe (seatIndex !) $ takeWhile (inRange bounds) rcs

        rays :: (Int, Int) -> [[(Int, Int)]]
        rays (r, c) = [[(r + dr*i, c + dc*i) | i <- dists] | dr <- [-1..1], dc <- [-1..1], (dr, dc) /= (0, 0)]

-- Given adjacency lists and maximum number of neighbors to tolerate, calculates
-- the eventual stable state, and returns the number of occupied seats.
solve :: [[Int]] -> Int -> Int
solve adjacencyLists maxNeighbors
    = length $ filter id $ elems $ fix nextState $ makeArray (repeat False)
    where
        makeArray :: [Bool] -> Array Int Bool
        makeArray = listArray (0, length adjacencyLists - 1)

        nextState :: Array Int Bool -> Array Int Bool
        nextState occupied = makeArray (zipWith update (elems occupied) adjacencyLists)
            where
                update occ adj =
                    null $ drop (if occ then maxNeighbors else 0) [idx | idx <- adj, occupied!idx]

        -- Iteratively calculates a fixed point of x: a value x' such that f x' == x'.
        fix :: Eq a => (a -> a) -> a -> a
        fix f x = let x' = f x in if x == x' then x else fix f x'

-- This problem could also be solved the with the generic Cellular Automaton
-- library (see CA.hs) but the current implementation using boolean arrays is
-- more efficient.

main = do
    input <- getContents
    let rcs = findCoords 'L' (lines input)
    print $ solve (getAdjacencyLists [1] rcs) 3
    print $ solve (getAdjacencyLists [1..] rcs) 4
