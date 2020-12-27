-- Support for single-state Cellular Automata with arbitrary neighborhoods.
module CA (CA, fromList, toList, evolve) where

import Data.List
import Data.Set (Set)
import qualified Data.Set as Set
import SortedList

-- A cellular automaton with coordinates of type `a`.
--
-- Internal representation: a sorted list of distinct active coordinates.
newtype CA a = CA{toList :: [a]}

-- Initialize a cellular automaton with given initial active cells.
fromList :: Ord a => [a] -> CA a
fromList = CA . distinct

-- Evolves a single generation of the cellular automaton.
--
-- `neighbors` is the neighbor function, from coordinates to a list of neighbor
-- coordinates. The result does not need to be sorted but elements must be
-- distinct!
--
-- `birth` and `survive` determine the number of active neighbors that causes
-- an inactive cell to become active, or an active cell to remain active,
-- respectively.
--
evolve :: Ord a => (a -> [a]) -> [Int] -> [Int] -> CA a -> CA a
evolve neighbors birth survive (CA active)
    = CA (merge newborn survived)
    where
        inactive = difference (distinct (concatMap neighbors active)) active

        newborn  = filter ((`elem` birth) . countActiveNeighbors) inactive

        survived = filter ((`elem` survive) . countActiveNeighbors) active

        activeSet = Set.fromList active

        countActiveNeighbors coords = length $ filter (`Set.member` activeSet) $ neighbors coords

-- Given two sorted lists, returns a merged sorted list.
merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge a@(x:xs) b@(y:ys)
    | x <= y    = x:merge xs b
    | otherwise = y:merge a ys
