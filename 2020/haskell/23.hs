import Control.Monad
import Control.Monad.ST
import Data.Char
import Data.Array.Unboxed
import Data.Array.ST

-- `simulate initialCups iterations` simulates several iterations of the cups
-- game using an implicit linked list represented as an integer array `next`,
-- such that next[i] is the number of the cup that comes after `i`.
--
-- `initialCups` must be a permutation of [1..length initialCups].
--
-- Executing a round of the game works as follows. We start from a current cup
-- `p`, and move the next three cups (called `a`, `b`, and `c`) to a destination
-- cup `r` (r = p - 1, except if p - 1 equals one of a, b, c, then r = p - 2,
-- except etc.)
--
-- In the linked list representation, that means we go from:
--
--    p -> a -> b -> c -> q   ...   r ----------------> s
--
-- To:
--
--    p ----------------> q   ...   r -> a -> b -> c -> s
--
-- which requires updating updating next[c] = s, next[p] = q, next[r] = a.
--
-- The result is an ordered list of cups after 1 (exclusive).
simulate :: [Int] -> Int -> [Int]
simulate initialCups iterations = extractResult 1 where
    rotate (x:xs) = xs ++ [x]

    len = length initialCups

    initialArrayElems = zip initialCups (rotate initialCups)

    decWrapping n = if n > 1 then n - 1 else len

    decSkipping n a b c
        | m == a || m == b || m == c = decSkipping m a b c
        | otherwise                  = m
        where m = decWrapping n

    extractResult i
        | j == 1    = []
        | otherwise = j:extractResult j
        where j = next ! i

    next :: UArray Int Int
    next = runSTUArray $ do
        next <- newArray_ (1, len)
        let getNext = readArray next
        let setNext = writeArray next
        mapM_ (uncurry setNext) initialArrayElems
        -- Note: second argument is the iteration number, which we don't
        -- need. Not sure if there's a way to avoid passing it...
        let iterate = \p _ -> do
            a <- getNext p
            b <- getNext a
            c <- getNext b
            q <- getNext c
            let r = decSkipping p a b c
            s <- getNext r
            setNext c s
            setNext p q
            setNext r a
            return q
        foldM_ iterate (head initialCups) [1..iterations]
        return next

main = do
    input <- getContents
    let [line] = lines input
    let cups = map digitToInt line
    -- Part 1
    putStrLn $ map intToDigit $ simulate cups 100
    -- Part 2
    print $ product $ take 2 $ simulate (cups ++ [length cups + 1..10^6]) (10^7)
