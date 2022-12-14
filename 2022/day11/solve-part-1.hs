import Data.Array
import Data.List
import Data.List.Split
--import System.IO.Unsafe  -- for debugging

-- Note: I assume that Int is 64 bits wide! If that doesn't hold, make sure to
-- replace Int with Integer (except maybe in the base-3 related functions)


-- Base 3 arithmetic functions. Lazy, so we only evaluate the digits we need.

toBase3 :: Int -> [Int]
toBase3 0 = []
toBase3 i = mod i 3:toBase3 (div i 3)

fromBase3 :: [Int] -> Int
fromBase3 [] = 0
fromBase3 (x:xs) = x + 3*(fromBase3 xs)

divBase3 :: [Int] -> (Int, [Int])
divBase3 [] = (0, [])
divBase3 (x:xs) = (x, xs)

addBase3 :: [Int] -> [Int] -> [Int]
addBase3 = go 0
  where
    go 0 [] [] = []
    go carry a b = mod sum 3 : go (div sum 3) aTail bTail
      where
        (aHead, aTail) = divBase3 a
        (bHead, bTail) = divBase3 b
        sum = aHead + bHead + carry

mulBase3 :: [Int] -> [Int] -> [Int]
mulBase3 [] _ = []
mulBase3 a  b = normalize 0 $ go [] b
  where
    go :: [[Int]] -> [Int] -> [Int]
    go []    []     = []
    go terms []     = let (sum, rest) = produceDigit terms in sum:go rest []
    go terms (b:bs) = let (sum, rest) = produceDigit (map (b*) a:terms) in sum:go rest bs

    produceDigit :: [[Int]] -> (Int, [[Int]])
    produceDigit nums = (sum (map head nums), filter (not.null) (map tail nums))

    normalize 0 [] = []
    normalize c [] = c `mod` 3:normalize (c `div` 3) []
    normalize c (x:xs) = let sum = x + c in sum `mod` 3:normalize (sum `div` 3) xs

-- Modulus m, multiplicative inverse of 3 in m
type Field = (Int, Int)

-- Value mod m, base-3 representation of the value
type Item = (Int, [Int])

-- I adapted this from: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
modularInverse :: Int -> Int -> Int
modularInverse m a = calc (a, 1, 0, m, 0, 1)
  where
    step :: (Int, Int, Int, Int, Int, Int) -> (Int, Int, Int, Int, Int, Int)
    step (old_r, old_s, old_t, r, s, t) = (r, s, t, old_r - q * r, old_s - q * s, old_t - q * t)
      where q = old_r `div` r

    calc arg@(old_r, old_s, old_t, r, s, t)
      | r == 0    = if old_r == 1 then old_s else failed
      | otherwise = calc $ step arg
      where failed = error $ "Failed to calculate modular inverse of " ++ show a ++ " modulo " ++ show m ++ " (are arguments coprime?)"

makeField :: Int -> Field
makeField mod = (mod, modularInverse mod 3)

makeItem :: Field -> Int -> Item
makeItem (m, _) i = (i `mod` m, toBase3 i)

divides :: Item -> Int -> Bool
divides (a, _) b = a `mod` b == 0

addInt :: Field -> Item -> Int -> Item
addInt (m, _) (a, b) c = ((a + c) `mod` m, b `addBase3` toBase3 c)

addSelf :: Field -> Item -> Item
addSelf (m, _) (a, b) = ((a + a) `mod` m, addBase3 b b)

mulInt :: Field -> Item -> Int -> Item
mulInt (m, _) (a, b) c = ((a * c) `mod` m, b `mulBase3` toBase3 c)

mulSelf :: Field -> Item -> Item
mulSelf (m, _) (a, b) = ((a * a) `mod` m, b `mulBase3` b)

div3 :: Field -> Item -> Item
div3 (m, i3) (a, b) = (((a - head) * i3) `mod` m, tail) where (head, tail) = divBase3 b

data Monkey = Monkey
  { mItems  :: [Int]
  , mUpdate :: Field -> Item -> Item
  , mDiv    :: Int
  , mPos    :: Int
  , mNeg    :: Int
  };

parseUpdate :: String -> (Field -> Item -> Item)
parseUpdate (sOp:' ':sArg)
  = case sArg of
    "old" -> case sOp of
      '+' -> addSelf
      '*' -> mulSelf
    s -> let b = read s in case sOp of
      '+' -> \f a -> addInt f a b
      '*' -> \f a -> mulInt f a b

parseMonkey :: [String] -> Monkey
parseMonkey [_, line1, line2, line3, line4, line5]
  = Monkey { mItems=items, mUpdate=update, mDiv=divisor, mPos=pos, mNeg=neg }
  where
    Just sItems  = stripPrefix "  Starting items: " line1
    Just sUpdate = stripPrefix "  Operation: new = old " line2
    Just sDiv    = stripPrefix "  Test: divisible by " line3
    Just sPos    = stripPrefix "    If true: throw to monkey " line4
    Just sNeg    = stripPrefix "    If false: throw to monkey " line5
    items = map read $ splitOn ", " sItems
    update = \f i -> div3 f (((parseUpdate sUpdate) f) i)
    divisor = read sDiv
    pos = read sPos
    neg = read sNeg
parseMonkey lines = error $ "Unable to parse lines: " ++ show lines

parseInput :: String -> [Monkey]
parseInput = map parseMonkey . splitOn [""] . lines

numRounds = 20

solve :: [Monkey] -> Int
solve monkeyList = monkeyBusiness
  where
    m = foldl1 lcm $ map mDiv monkeyList
    f = makeField m

    numMonkeys = length monkeyList

    monkeys :: Array Int Monkey
    monkeys = listArray (0, numMonkeys - 1) monkeyList

    -- A list of pairs of initial <monkey index, item value> pairs
    monkeyItems :: [(Int, Item)]
    monkeyItems = [(index, makeItem f item) | (index, Monkey{mItems=items}) <- assocs monkeys, item <- items]

    itemPositions :: [(Int, Item)]
    itemPositions = concat $ map (takeRounds numRounds . iterate play) monkeyItems

    -- Given a <monkey index, item value> pair, updates the item value and
    -- calculates the next monkey index.
    play :: (Int, Item) -> (Int, Item)
    play (index, item) = (index', item')
      where
        Monkey{mUpdate=update, mDiv=divisor, mPos=pos, mNeg=neg} = monkeys ! index
        item'  = update f item
        index' = if item' `divides` divisor then pos else neg

    -- Truncates the infinite list of <monkey, item> pairs to the first given number of round.
    -- A new round starts whenever the next monkey index is less than the previous one.
    takeRounds :: Int -> [(Int, Item)] -> [(Int, Item)]
    takeRounds 0 _  = []
    takeRounds n (head@(i, _):tail@((j, _):_)) = head:takeRounds n' tail
      where n' = if i <= j then n else n - 1

    -- For each monkey, the number of items it has handled
    itemsHandled :: [Int]
    itemsHandled = elems a
      where
        a  = accumArray f 0 (0, numMonkeys - 1) itemPositions
        f cnt _ = cnt + 1

    -- The "monkey business" is the product of the two largest number of items handled by any monkeys
    monkeyBusiness = foldl1 (*) $ take 2 $ reverse $ sort itemsHandled

main = interact ((++ "\n") . show . solve . parseInput)
