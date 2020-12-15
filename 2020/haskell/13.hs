import Data.List
import Data.List.Split

parseSchedule :: String -> [Maybe Int]
parseSchedule = map parsePart . splitOn ","
    where
        parsePart "x" = Nothing
        parsePart s   = Just (read s)

solvePart1 :: Int -> [Maybe Int] -> Int
solvePart1 startTime periods = (min_time - startTime) * period
    where
        (min_time, period) = minimum [((startTime `divUp` p) * p, p) | Just p <- periods]

        -- Integer division, like `div`, but rounding up instead.
        divUp a b = (a + b - 1) `div` b

solvePart2 :: [Maybe Int] -> Integer
solvePart2 periods = t
    where
        (t, _) = foldl' update (0, 1) fullSchedule

        -- List of (index, period) pairs, which are the remainders and divisors.
        fullSchedule :: [(Integer, Integer)]
        fullSchedule = [(toInteger i, toInteger p) | (i, Just p) <- zip [0..] periods]

        -- Given start time t, multiplier m, remainder i and divisor p,
        -- calculates t' and m', so that m' = m * p and  t' = t + k * m has
        -- remainder i modulo p.
        update :: (Integer, Integer) -> (Integer, Integer) -> (Integer, Integer)
        update (t, m) (i, p) = (
            head $ dropWhile (\t -> (t + i) `mod` p /= 0) $ iterate (+ m) t,
            m * p)

main = do
    input <- getContents
    let [startTimeString, scheduleString] = lines input
    let startTime = read startTimeString
    let schedule = parseSchedule scheduleString
    print $ solvePart1 startTime schedule
    print $ solvePart2 schedule
