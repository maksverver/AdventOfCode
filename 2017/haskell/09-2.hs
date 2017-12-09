data BlockData = Block [BlockData] | BlockGarbage String deriving Show

parseGarbage :: String -> (String, String)
parseGarbage ('>':rest) = ("", rest)
parseGarbage ('!':ch:rest) = parseGarbage rest
parseGarbage (ch:rest) = (ch:restData, restInput)
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
parseBlock (',':rest) = parseBlock rest

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
        evalBlock (BlockGarbage contents) = length contents

main = do
    input <- getLine
    let block = parse input
    print $ calculateScore block
    print $ countGarbage block
