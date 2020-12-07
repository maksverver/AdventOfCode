import qualified Data.Map.Strict as Map
import qualified Data.Set as Set
import Data.List
import Data.Maybe

type Bag = (String, [(Int, String)])  -- outer_kind -> ([count, inner_kind])

parseBag :: String -> Bag
parseBag line = (label a b, parseRest rest)
    where
        a:b:"bags":"contain":rest = words $ filter (not . (`elem` ".,")) line

        parseRest [] = []
        parseRest ["no", "other", "bags"] = []
        parseRest (n:a:b:bags:rest)
            | bags `elem` ["bag", "bags"] = (read n, label a b):parseRest rest

        label a b = a ++ " " ++ b

breadthFirstSearch :: Ord a => (a -> [a]) -> [a] -> [a]
breadthFirstSearch successor initial = concat $ process (Set.fromList initial) initial
    where
        process seen []   = []
        process seen todo = todo : process seen' todo'
            where (seen', todo') = deduplicate seen (concatMap successor todo)

        deduplicate s [] = (s, [])
        deduplicate s (x:xs)
            | Set.member x s = deduplicate s xs
            | otherwise      = (s', x:xs') where (s', xs') = deduplicate (Set.insert x s) xs

findAllContainers :: [Bag] -> String -> [String]
findAllContainers bags kind = tail $ breadthFirstSearch findContainers [kind]
    where
        findContainers :: String -> [String]
        findContainers kind = Map.findWithDefault [] kind containerMap

        containerMap :: Map.Map String [String]
        containerMap = Map.fromListWith(++) [(inner, [outer]) | (outer, contents) <- bags, (_, inner) <- contents]

contentSize :: [Bag] -> String -> Int
contentSize bags kind = fst $ contentSize' kind Map.empty
    where
        contentSize' :: String -> Map.Map String Int -> (Int, Map.Map String Int)
        contentSize' kind memo
            = case Map.lookup kind memo of
                Just size -> (size, memo)
                Nothing   -> foldl' calculate (0, memo) contents
            where
                Just contents = Map.lookup kind containsMap 
                calculate (size, memo) (count, kind)
                    = (size + (size' + 1)*count, memo')
                    where (size', memo') = contentSize' kind memo

        containsMap :: Map.Map String [(Int, String)]
        containsMap = Map.fromList bags

main = do
    input <- getContents
    let bags = map parseBag (lines input) 
    print $ length $ findAllContainers bags "shiny gold"
    print $ contentSize bags "shiny gold"
