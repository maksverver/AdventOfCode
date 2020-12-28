module Deque where

import qualified Prelude
import Prelude hiding (reverse)

type Deque a = ([a], [a])

empty :: Deque a
empty = ([], [])

isEmpty :: Deque a -> Bool
isEmpty ([], []) = True
isEmpty _        = False

fromList :: [a] -> Deque a
fromList xs = (xs, [])

toList :: Deque a -> [a]
toList (xs, ys) = xs ++ Prelude.reverse ys

reverse :: Deque a -> Deque a
reverse (xs, ys) = (ys, xs)

addBack :: a -> Deque a -> Deque a
addBack v (xs, ys) = (xs, v:ys)

removeFront :: Deque a -> (a, Deque a)
removeFront (x:xs, ys) = (x, (xs, ys))
removeFront ([], []) = error "empty Deque"
removeFront ([], ys) = let x:xs = Prelude.reverse ys in (x, (xs, []))

addFront :: a -> Deque a -> Deque a
addFront v d = reverse $ addBack v $ reverse d

removeBack :: Deque a -> (a, Deque a)
removeBack d = let (v, d') = removeFront (reverse d) in (v, reverse d')
