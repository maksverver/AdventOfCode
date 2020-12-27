module PairWiseAssociation where

import Data.Bifunctor
import Data.List

{-
Finds a one-to-one mapping between key and value pairs, using the process
of elimination.

Input is a list of pairs, where each pair consists of a list of possible keys
(without duplicates) and a single value. The output is a unique (key, value)
mapping. Note that the ordering of the output is unspecified.

The way this works is by searching for a value with a single key remaining; this
key is then associated with its value, and the key is removed as a possibility
for all other values. Then, another value should have a single key remaining and
so on.

If there is no solution this function just fails with an error. Note that since
the result is product iteratively, it's possible to consume a prefix of the
result if the full result is not necessary (e.g. to find the value associated
with one specific key).
-}
solvePairs :: Eq k => [([k], v)] -> [(k, v)]
solvePairs [] = []
solvePairs keys = (key, val) : solvePairs (map (first (delete key)) rest)
    where
        ((key, val), rest) = isolateSingle keys

        isolateSingle :: [([k], v)] -> ((k, v), [([k], v)])
        isolateSingle (([], _):_) = error "no possible keys left"
        isolateSingle (([key], val):rest) = ((key, val), rest)
        isolateSingle (first:rest) = (single, first:rest')
            where (single, rest') = isolateSingle rest
        isolateSingle [] = error "no unique key found"
