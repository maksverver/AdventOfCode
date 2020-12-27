module SortedList where

import Data.List (nub, sort, foldl')

-- Given a list, returns a sorted list of unique elements.
--
-- For example:
--
--  distinct [3, 1, 4, 1, 5, 9, 2] == [1, 2, 3, 4, 5, 9]
--
distinct :: Ord a => [a] -> [a]
distinct = nub . sort

-- Returns the union of two sorted lists.
union :: Ord a => [a] -> [a] -> [a]
union xs [] = xs
union [] ys = ys
union (x:xs) (y:ys)
    | x < y = x:union xs (y:ys)
    | x > y = y:union (x:xs) ys
    | otherwise = x:union xs ys

-- Returns the intersection of two sorted lists.
intersection :: Ord a => [a] -> [a] -> [a]
intersection xs [] = []
intersection [] ys = []
intersection (x:xs) (y:ys)
    | x < y = intersection xs (y:ys)
    | x > y = intersection (x:xs) ys
    | otherwise = x:intersection xs ys

-- Returns the union of zero or more sorted lists.
--
-- Note: this could be made more efficient by grouping lists of similar sizes.
unionAll :: Ord a => [[a]] -> [a]
unionAll [] = []
unionAll (l:ls) = foldl' union l ls

-- Returns the intersection of one or more sorted lists.
--
-- Note: this could be made more efficient by grouping lists of similar sizes.
intersectionAll :: Ord a => [[a]] -> [a]
intersectionAll [] = error "intersection of nothing is undefined"
intersectionAll (l:ls) = foldl' intersection l ls

-- Returns the set difference of two sorted lists.
--
-- In other words, given arguments a and b, this returns a list with the
-- elements of `a` (in their original order) without the elements of `b`.
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
