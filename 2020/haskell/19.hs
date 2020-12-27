import Data.Array
import Data.Bifunctor
import Data.List.Split
import Data.Maybe

data RawRule = RawLeaf String | RawNode [[Int]] deriving Show

data Rule = Leaf String | Node [[Rule]] deriving Show

parseRule :: String -> (Int, RawRule)
parseRule line = (read numDef, parseRawRule ruleDef)
    where
        [numDef, ruleDef] = splitOn ": " line

        parseRawRule s
            | head s == '"' && last s == '"' = RawLeaf $ tail $ init s
            | otherwise = RawNode $ map (map read . words) $ splitOn " | " s

cookRules :: [(Int, RawRule)] -> Array Int Rule
cookRules rawRules = arr
    where
        nums = map fst rawRules
        lo = minimum nums
        hi = maximum nums
        arr = array (lo, hi) (map (second cook) rawRules)

        cook :: RawRule -> Rule
        cook (RawLeaf s) = Leaf s
        cook (RawNode alts) = Node (map (map (arr!)) alts)

-- `stripPrefix s t` returns `Just u` if `t == s ++ u`, or `Nothing` if `t` does
-- not start with `s`.
stripPrefix :: String -> String -> Maybe String
stripPrefix [] t  = Just t
stripPrefix _  [] = Nothing
stripPrefix (x:xs) (y:ys)
    | x == y    = stripPrefix xs ys
    | otherwise = Nothing

-- `matchesEntirely rule line` returns whether `rule` can match `line` entirely.
--
-- Implementation note: the implementation here is very inefficient if the input
-- grammar is ambiguous (i.e., there are multiple derivations possible)! To fix
-- this, `match` and `matchSeq` should be changed to return distinct suffixes
-- only, which probably requires returning the (integer) match length too,
-- because deduplicating string prefixes is inefficent too.
matchesEntirely :: Rule -> String -> Bool
matchesEntirely rule line = any null (match rule line)
    where
        -- `match r s` returns a list of suffixes of `s` for which rule `r`
        -- matches the corresponding prefix.
        match :: Rule -> String -> [String]
        match (Leaf s) t = maybeToList (stripPrefix s t)
        match (Node alts) t = concatMap (`matchSeq` t) alts

        -- `matchSeq rs s` returns a list of suffixes obtained after matching
        -- each of the rules `rs` against `s` in sequence.
        matchSeq :: [Rule] -> String -> [String]
        matchSeq [] s = [s]
        matchSeq (r:rs) s = concatMap (matchSeq rs) (match r s)

main = do
    input <- getContents
    let [ruleDefs, messages] = splitOn [[]] (lines input)
    let rawRules = map parseRule ruleDefs
    let rule1 = cookRules rawRules ! 0
    let rule2 = cookRules (map fixPart2 rawRules) ! 0
    print $ length $ filter (matchesEntirely rule1) messages
    print $ length $ filter (matchesEntirely rule2) messages

    where
        fixPart2 (8, r)  = (8, fixRule8 r)
        fixPart2 (11, r) = (11, fixRule11 r)
        fixPart2 elem    = elem

        fixRule8 (RawNode [[42]]) = RawNode [[42], [42, 8]]

        fixRule11 (RawNode [[42, 31]]) = RawNode [[42, 31], [42, 11, 31]]
