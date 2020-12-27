import qualified CA
import Data.List

type Coords = (Int, Int)

data Dir = NW | NE | W | E | SW | SE deriving (Bounded, Enum, Show);

step :: Coords -> Dir  -> Coords
step (r, c) NW = (r - 1, c - 1)
step (r, c) NE = (r - 1, c    )
step (r, c) W  = (r    , c - 1)
step (r, c) E  = (r    , c + 1)
step (r, c) SW = (r + 1, c    )
step (r, c) SE = (r + 1, c + 1)

tokenizePath :: String -> [Dir]
tokenizePath [] = []
tokenizePath s = dir:tokenizePath s'
    where
        (dir, s') = case s of
            ('n':'w':s') -> (NW, s')
            ('n':'e':s') -> (NE, s')
            ('w':    s') -> (W,  s')
            ('e':    s') -> (E,  s')
            ('s':'w':s') -> (SW, s')
            ('s':'e':s') -> (SE, s')

parsePath :: String -> Coords
parsePath = foldl' step (0, 0) . tokenizePath

neighbors :: Coords -> [Coords]
neighbors p = map (step p) [minBound..maxBound]

main = do
    input <- getContents
    let inputCoords = map parsePath $ lines input :: [(Int, Int)]
    -- Initially, tiles are flipped if they occur in the input an odd number of times.
    let initialCoords = [head ps | ps <- group $ sort $ inputCoords, length ps `mod` 2 == 1]
    print $ length initialCoords -- part 1
    let generations = iterate (CA.evolve neighbors [2] [1,2]) (CA.fromList initialCoords)
    print $ length $ CA.toList $ generations !! 100 -- part 2

