import qualified CA

type Coords = (Int, Int, Int, Int)

neighbors3D :: Coords -> [Coords]
neighbors3D (x, y, z, w) = [
        (x + dx, y + dy, z + dz, w) |
        dx <- [-1..1], dy <- [-1..1], dz <- [-1..1],
        dx /= 0 || dy /= 0 || dz /= 0]

neighbors4D :: Coords -> [Coords]
neighbors4D (x, y, z, w) = [
        (x + dx, y + dy, z + dz, w + dw) |
        dx <- [-1..1], dy <- [-1..1], dz <- [-1..1], dw <- [-1..1],
        dx /= 0 || dy /= 0 || dz /= 0 || dw /= 0]

main = do
    input <- getContents
    let initial = CA.fromList [(r, c, 0, 0) |
            (r, line) <- zip [0..] (lines input),
            (c, char) <- zip [0..] line,
            char == '#']

    print $ length $ CA.toList $ iterate (CA.evolve neighbors3D [3] [2, 3]) initial !! 6
    print $ length $ CA.toList $ iterate (CA.evolve neighbors4D [3] [2, 3]) initial !! 6
