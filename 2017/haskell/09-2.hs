data GarbageData = GarbageChar Char | EscapedChar Char deriving Show
data BlockData = Block [BlockData] | BlockChar Char | BlockGarbage [GarbageData] deriving Show

parseGarbage :: String -> ([GarbageData], String)
parseGarbage ('>':rest) = ([], rest)
parseGarbage ('!':ch:rest) = (EscapedChar ch:restData, restInput)
    where (restData, restInput) = parseGarbage rest
parseGarbage (ch:rest) = (GarbageChar ch:restData, restInput)
    where (restData, restInput) = parseGarbage rest

parseBlock :: String -> ([BlockData], String)
parseBlock ('}':rest) = ([], rest)
parseBlock ('<':rest) = (BlockGarbage garbageData:restData, restInput')
    where
        (garbageData, restInput) = parseGarbage rest
        (restData, restInput') = parseBlock restInput
parseBlock ('{':rest) = (Block blockData:restData, restInput')
    where
        (blockData, restInput) = parseBlock rest
        (restData, restInput') = parseBlock restInput
parseBlock (ch:rest) = (BlockChar ch:restData, restInput)
    where (restData, restInput) = parseBlock rest

parse :: String -> [BlockData]
parse ('{':rest) = contents
    where output@(contents, "") = parseBlock rest

calculateScore :: [BlockData] -> Int
calculateScore = score 1
    where
        score depth contents = depth + sum (map evalBlock contents)
            where
                evalBlock (Block contents) = score (depth + 1) contents
                evalBlock _ = 0

countGarbage :: [BlockData] -> Int
countGarbage contents = sum (map evalBlock contents)
    where
        evalBlock (Block contents) = sum (map evalBlock contents)
        evalBlock (BlockGarbage contents) = sum (map evalGarbage contents)
        evalBlock _ = 0
        evalGarbage (GarbageChar _) = 1
        evalGarbage _ = 0

main = do
    input <- getLine
    let block = parse input
    print $ calculateScore block
    print $ countGarbage block
