import Data.Function
import Data.List
import Data.List.Split

data Tile = Tile{
    tileId   :: Int,
    topId    :: Int,
    bottomId :: Int,
    leftId   :: Int,
    rightId  :: Int,
    interior :: [String]} deriving Show

-- Rotates a 2D grid clockwise by 90 degrees.
rotate :: [String] -> [String]
rotate xs
    | all null xs = []
    | otherwise   = reverse (map head xs):rotate (map tail xs)

parseTile :: [String] -> (Int, [String])
parseTile (('T':'i':'l':'e':' ':s):rows) | last s == ':' = (read (init s), rows)

-- Given a 2D grid, returns the 8 variations obtained by rotation and mirroring.
transformations :: [String] -> [[String]]
transformations x = [z | y <- [x, reverse x], z <- take 4 (iterate rotate y)]

-- Given a tile id and an initial grid, generates all 8 variations of the tile.
processTile :: (Int, [String]) -> [Tile]
processTile (tileId, grid)
    = [Tile{
            tileId   = tileId,
            topId    = sideId (head grid'),
            bottomId = sideId (last grid'),
            leftId   = sideId (map head grid'),
            rightId  = sideId (map last grid'),
            interior = map (init . tail) $ init $ tail grid'} |
        grid' <- transformations grid]
    where
        -- Interprets a string as a binary number with '#' as 1.
        -- For example, makeId "##.#" == 13.
        sideId :: String -> Int
        sideId = foldl' (\acc ch -> 2*acc + fromEnum (ch == '#')) 0

-- Deletes all variants of `tile` from `tiles` with the same tile id.
deleteTiles :: Tile -> [Tile] -> [Tile]
deleteTiles tile tiles = [t | t <- tiles, tileId t /= tileId tile]

matchTiles :: (Tile -> Tile -> Bool) -> [Tile] -> Tile-> ([Tile], [Tile])
matchTiles match remainingTiles tile = (remainingTiles', tile:tiles')
    where
        (remainingTiles', tiles') = case [t | t <- remainingTiles, match tile t] of
            []         -> (remainingTiles, [])
            [nextTile] -> matchTiles match (deleteTiles nextTile remainingTiles) nextTile
            _          -> error "multiple matches possible"

createColumn :: [Tile] -> Tile -> ([Tile], [Tile])
createColumn = matchTiles (\a b -> bottomId a == topId b)

createRow :: [Tile] -> Tile -> ([Tile], [Tile])
createRow = matchTiles (\a b -> rightId a == leftId b)

-- `stitchRows remainingTiles firstColumn` expands the first column into a full grid of tiles,
-- using `createRow` to expand the leftmost tile of each row into a full row of tiles.
--
-- We could double-check that tiles in columns beyond the first also match along up/down edge,
-- but for now we'll assume that's the case.
stitchRows :: [Tile] -> [Tile] -> ([Tile], [[Tile]])
stitchRows remainingTiles [] = (remainingTiles, [])
stitchRows remainingTiles (tile:tiles) = (remainingTiles'', row:rows)
    where
        (remainingTiles', row) = createRow remainingTiles tile
        (remainingTiles'', rows) = stitchRows remainingTiles' tiles

identifyMonsters :: [String] -> [String]
identifyMonsters []   = []
identifyMonsters grid = identifyHorizontal (head grid : identifyMonsters (tail grid))
    where
        identifyHorizontal :: [String] -> [String]
        identifyHorizontal grid
            | all null grid = grid
            | otherwise     = identifyHere (
                zipWith (:) (map head grid) (identifyHorizontal (map tail grid)))

        identifyHere :: [String] -> [String]
        identifyHere grid
            | detectMonster grid = imposeMonster grid
            | otherwise          = grid

        detectMonster :: [String] -> Bool
        detectMonster = matchAll monster
            where
                matchAll [] _ = True
                matchAll _ [] = False
                matchAll (a:monster) (b:grid) = matchRow a b && matchAll monster grid

                matchRow []          _       = True
                matchRow _           []      = False
                matchRow (a:monster) (b:row) =
                    (a /= '#' || b == '#'|| b == 'O') && matchRow monster row

        imposeMonster :: [String] -> [String]
        imposeMonster = imposeAll monster
            where
                imposeAll []          grid     = grid
                imposeAll (a:monster) (b:grid) = imposeRow a b:imposeAll monster grid

                imposeRow []          row     = row
                imposeRow (a:monster) (b:row) =
                    (if a == '#' then 'O' else b):imposeRow monster row

        monster :: [String]
        monster = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "]

main = do
    input <- getContents
    let tiles = concatMap (processTile . parseTile) $ filter (/= []) $ splitOn [[]] $ lines input

    -- Find corner tiles (note: each corner appears twice in the list due to mirroring!)
    let corners = [t | t <- tiles,
            null [t' | t' <- tiles,
                    tileId t /= tileId t', topId t == bottomId t' || leftId t == rightId t']]

    -- Part 1: print product of corner tile ids
    print $ product $ nub $ map tileId corners

    -- Part 2: reconstruct grid and find monsters.
    let corner = head corners :: Tile
    let ([], tileGrid) = uncurry stitchRows $ createColumn (deleteTiles corner tiles) corner
    let compositeGrid = concatMap (map concat . transpose . map interior) tileGrid :: [String]
    -- There should be exactly one orientation that has some monsters in it.
    let [orientedGrid] = [grid |
            grid <- map identifyMonsters $ transformations compositeGrid, 'O' `elem` concat grid]
    print $ length $ filter ('#' ==) $ concat orientedGrid
