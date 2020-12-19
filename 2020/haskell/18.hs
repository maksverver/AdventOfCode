import Data.Char
import Data.List

data Tok = Digit Int | LParen | RParen | Plus | Asterisk deriving (Show, Eq);

tokenize :: String -> [Tok]
tokenize str = map token $ filter (not . isSpace) str
    where
        token :: Char -> Tok
        token ch
            | isDigit ch = Digit (read [ch])
            | ch == '('  = LParen
            | ch == ')'  = RParen
            | ch == '+'  = Plus
            | ch == '*'  = Asterisk

{-
For part 1, implement a recursive descent parser for the following grammar,
which is carefully written to ensure it's not left-recursive:

    Complex = Base Rest
    Rest    = (Plus | Asterisk) Base Rest
    Base    = Digit | LParen Complex RParen

We have to pass an accumulator to each parse function because both operators are
left-associative.
-}
solve1 :: [Tok] -> Int
solve1 tokens = let (i, []) = parseComplex tokens in i
    where
        parseComplex :: [Tok] -> (Int, [Tok])
        parseComplex tokens = let (i, tokens') = parseBase tokens in parseRest i tokens'

        parseRest :: Int -> [Tok] -> (Int, [Tok])
        parseRest acc tokens = case tokens of
            (Plus:rest)     -> let (i, tokens') = parseBase rest in parseRest (acc + i) tokens'
            (Asterisk:rest) -> let (i, tokens') = parseBase rest in parseRest (acc * i) tokens'
            _               -> (acc, tokens)

        parseBase :: [Tok] -> (Int, [Tok])
        parseBase (Digit i:tokens') = (i, tokens')
        parseBase (LParen:tokens')  = let (i, RParen:tokens'') = parseComplex tokens' in (i, tokens'')

{-
Part 2 is actually somewhat simpler, because giving addition precedence over
multiplication allows us to remove the accumulator. This works because both
addition and multiplication are associative operations, so long as we don't
mix them (as in part 1) it doesn't matter if we evaluate them left-to-right or
right-to-left.

The grammar looks like this:

    Product = Sum | Sum Asterisk Product
    Sum     = Base | Base Plus Sum
    Base    = Digit | LParen Complex RParen
-}
solve2 :: [Tok] -> Int
solve2 tokens = let (i, []) = parseProduct tokens in i
    where
        parseProduct :: [Tok] -> (Int, [Tok])
        parseProduct tokens = let result@(i, tokens') = parseSum tokens in case tokens' of
            (Asterisk:rest) -> let (j, tokens'') = parseProduct rest in (i * j, tokens'')
            _               -> result

        parseSum :: [Tok] -> (Int, [Tok])
        parseSum tokens = let result@(i, tokens') = parseBase tokens in case tokens' of
            (Plus:rest) -> let (j, tokens'') = parseSum rest in (i + j, tokens'')
            _           -> result

        parseBase :: [Tok] -> (Int, [Tok])
        parseBase (Digit i:tokens') = (i, tokens')
        parseBase (LParen:tokens')  = let (i, RParen:tokens'') = parseProduct tokens' in (i, tokens'')

main = do
    input <- getContents
    let tokens = map tokenize (lines input)
    print $ sum $ map solve1 tokens
    print $ sum $ map solve2 tokens
