import Data.List
import Data.List.Split
import PairWiseAssociation

data Range = Range Int Int deriving Show

data Field = Field {
    fieldKey :: String,
    fieldRanges :: [Range]} deriving Show

instance Eq Field where
    (==) Field{fieldKey=k1} Field{fieldKey=k2} = k1 == k2

type Ticket = [Int]

parseRange :: String -> Range
parseRange word | a <= b = Range a b where [a, b] = map read $ splitOn "-" word

parseField :: String -> Field
parseField line = Field key ranges
    where
        [key, rangeDefs] = splitOn ": " line
        ranges = map parseRange $ splitOn " or " rangeDefs

parseTicket :: String -> Ticket
parseTicket line = map read $ splitOn "," line

inRange :: Int -> Range -> Bool
inRange x (Range a b) = a <= x && x <= b

inAnyRange :: Int -> [Range] -> Bool
inAnyRange value = any (inRange value)

invalidValues :: [Field] -> Ticket -> [Int]
invalidValues fields = filter (not . (`inAnyRange` ranges))
    where
        ranges = concatMap fieldRanges fields

totalErrors :: [Field] -> [Ticket] -> Int
totalErrors fields tickets = sum $ concatMap (invalidValues fields) tickets

isValidTicket :: [Field] -> Ticket -> Bool
isValidTicket fields = null . invalidValues fields

-- Uses the ranges from `fields` and the values from `tickets` to determine
-- which field corresponds with which position on the ticket, and returns a
-- list of fields paired with corresponding elements from `xs`.
--
-- For example, associateFields fields tickets [0..] will return a list of
-- (field, position) pairs, but not necessarily ordered by position.
--
-- In the solution below, we'll directly associate fields with ticket values,
-- bypassing the need to index lists by positions.
--
-- (We assume all field positions can be uniquely determined, which is true for
-- the given test data, but not strictly necessary for the problem, since we
-- only need to identify a subset of fields.)
associateFields :: [Field] -> [Ticket] -> [a] -> [(Field, a)]
associateFields fields tickets xs
    = solvePairs $ zip (map possibilities $ transpose tickets) xs
    where
        -- Returns a list of possible fields based on initial ticket values.
        possibilities :: [Int] -> [Field]
        possibilities values = filter possible fields
            where possible field = all (`inAnyRange` (fieldRanges field)) values

main = do
    input <- getContents
    let [part1, part2, part3] = splitOn [[]] (lines input)
    let fields = map parseField part1
    let yourTicket = let ["your ticket:", def] = part2 in parseTicket def
    let nearbyTickets = let ("nearby tickets:":defs) = part3 in map parseTicket defs

    -- Part 1: count sum of invalid ticket values.
    print $ totalErrors fields nearbyTickets

    -- Part 2: identifiy field positions and calculate product of "departure" fields.
    let validTickets = filter (isValidTicket fields) nearbyTickets
    let departureValues = [value |
            (field, value) <- associateFields fields validTickets yourTicket,
            "departure " `isPrefixOf` (fieldKey field)]
    print $ product departureValues
