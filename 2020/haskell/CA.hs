-- Support for single-state Cellular Automata with arbitrary neighborhoods.
module CA (CA, fromList, toList, evolve) where

import Data.List
import Data.Set (Set)
import qualified Data.Set as Set

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

-- Given a list, returns a sorted list of unique elements.
--
-- For example:
--
--  distinct [3, 1, 4, 1, 5, 9, 2] == [1, 2, 3, 4, 5, 9]
--
distinct :: Ord a => [a] -> [a]
distinct = nub . sort

-- Given two sorted lists, a and b, returns a list with the elements of `a`
-- (in their original order) without the elements of `b`. This also works
-- correctly with duplicates, although that's not used in this module.
--
-- For example:
--
--  difference [1, 2, 3] [2, 4, 6] == [1, 3]
--  difference [1, 2, 2, 3, 3, 3] [1, 1, 2, 2, 3, 3] == [3]
--
difference :: Ord a => [a] -> [a] -> [a]
difference xs [] = xs
difference [] _  = []
difference a@(x:xs) b@(y:ys)
    | x < y     = x:difference xs b
    | y < x     = difference a ys
    | otherwise = difference xs ys

-- Given two sorted lists, returns a merged sorted list.
merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge a@(x:xs) b@(y:ys)
    | x <= y    = x:merge xs b
    | otherwise = y:merge a ys
