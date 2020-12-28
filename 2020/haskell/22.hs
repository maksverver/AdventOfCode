import Data.Char
import Data.List
import Data.List.Split
import Data.Maybe
import Deque (Deque)
import qualified Deque

type Deck = Deque Int
type State = (Deck, Deck)

score :: State -> Int
score state = sum $ zipWith (*) [1..] (Deque.toList $ Deque.reverse deck)
    where Just deck = winningDeck state

winningDeck :: State -> Maybe Deck
winningDeck (h1, h2)
    | Deque.isEmpty h1 = Just h2
    | Deque.isEmpty h2 = Just h1
    | otherwise        = Nothing

isOver :: State -> Bool
isOver = isJust . winningDeck

solvePart1 :: State -> State
solvePart1 = until isOver playRound
    where
        playRound :: State -> State
        playRound (h1, h2)
            | c1 > c2 = (Deque.addBack c2 $ Deque.addBack c1 h1', h2')
            | c2 > c1 = (h1', Deque.addBack c1 $ Deque.addBack c2 h2')
            where
                (c1, h1') = Deque.removeFront h1
                (c2, h2') = Deque.removeFront h2

-- Returns the final state, or Nothing if the game loops. In the latter case we
-- don't know the final decks, but that's not a problem unless the loop occurs
-- at the top level, which doesn't happen with the given test data. If it did,
-- more complicated cycle detection would be necessary.
--
-- Note: solvePart2 may be invoked recursively with the same state. We could
-- optimize it with memoization, but this doesn't seem to be necessary for the
-- official test data. Note that infinite recursion is not possible because each
-- subgame uses strictly fewer cards than before.
solvePart2 :: State -> Maybe State
solvePart2 = findEnd . iterate playRound
    where
        -- findEnd detects cycles similar to Floyd's Tortoise & Hare algorithm.
        -- We don't necessarily find the first duplicate; if the first duplicate
        -- occurs at 1-based index N, we may evaluate up to 2N list elements.
        findEnd :: [State] -> Maybe State
        findEnd states = go states states
            where
                go (x:xs) (y1:y2:ys)
                    | isOver y1 = Just y1
                    | isOver y2 = Just y2
                    | x == y2   = Nothing  -- duplicate state detected!
                    | otherwise = go xs ys

        playRound :: State -> State
        playRound (h1, h2)
            | player1Won = (Deque.addBack c2 $ Deque.addBack c1 h1', h2')
            | otherwise  = (h1', Deque.addBack c1 $ Deque.addBack c2 h2')
            where
                (c1, h1') = Deque.removeFront h1
                (c2, h2') = Deque.removeFront h2

                player1Won
                    = if c1 > length l1 || c2 > length l2 then c1 > c2 else case subgame of
                        Nothing       -> True  -- player 1 wins in case of a loop
                        Just (r1, r2) -> Deque.isEmpty r2
                    where
                        l1 = take c1 (Deque.toList h1')
                        l2 = take c2 (Deque.toList h2')
                        subgame = solvePart2 (Deque.fromList l1, Deque.fromList l2)

main = do
    input <- getContents
    let ["Player 1:":part1, "Player 2:":part2] = splitOn [[]] (lines input)
    let hand1 = map read part1 :: [Int]
    let hand2 = map read part2 :: [Int]
    let state = (Deque.fromList hand1, Deque.fromList hand2) :: State
    print $ score $ solvePart1 state
    print $ score $ fromJust $ solvePart2 state
