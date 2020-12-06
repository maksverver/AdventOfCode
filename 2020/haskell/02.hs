import Data.Char

-- Parses a string of the form "1-23 x: abc" into a tuple (1, 2, 'x', "abc").
parse :: String -> (Int, Int, Char, String)
parse s = (i, j, c, t)
    where
        (i, '-':s') = parseIntPrefix s
        (j, ' ':c:':':' ':t) = parseIntPrefix s'

        parseIntPrefix :: String -> (Int, String)
        parseIntPrefix s = (read (takeWhile isDigit s), dropWhile isDigit s)

-- Checks that `c` occurs between `i` and `j` times in `s`
valid1 (i, j, c, s) = i <= k && k <= j where k = length $ filter (==c) s

-- Checks that `c` occurs at exactly one of 1-based index `i` or `j` in `s`.
valid2 (i, j, c, s) = ((s !! (i - 1)) == c) /= ((s !! (j - 1)) == c)

main = do
    input <- getContents
    let records = map parse (lines input)
    print $ length $ filter valid1 records
    print $ length $ filter valid2 records
