import Data.Bits
import Data.Char
import Data.IntMap (IntMap)
import qualified Data.IntMap.Strict as IntMap
import Data.List

-- Note: this solution uses Int to store addresses/values under the assumption
-- that Int is at least 36 bits wide. Using Int64 instead is not an option
-- because there is no Int64Map. Therefore, this solution will not work on
-- 32-bit systems.

data Instr = SetMask String | Store Int Int deriving Show

parseInstr :: String -> Instr
parseInstr ('m':'a':'s':'k':' ':'=':' ':s) = SetMask s
parseInstr ('m':'e':'m':'[':s) = Store (read addr) (read value)
    where
        addr = takeWhile isDigit s
        (']':' ':'=':' ':value) = dropWhile isDigit s

-- Interprets binary string using `one` as the character representing 1 (all
-- others are considered zero). For example: `interpret 'a' "abca" == 9`.
interpret :: Char -> String -> Int
interpret one = foldl' (\acc ch -> 2 * acc + fromEnum (ch == one)) 0

-- Given an integer, returns a list of all integers with a subset of bits set.
-- For example: `submasks 5 == [5, 4, 1, 0]` (in binary: 101, 100, 001, 000).
submasks :: Int -> [Int]
submasks template = gen template
    where
        gen 0 = [0]
        gen i = i:gen ((i - 1) .&. template)


-- Part 1 implementation

type Machine1 = ({-mem-} IntMap Int, {-mask-} Int, {-ones-} Int)

init1 = (IntMap.empty, 0, 0) :: Machine1

update1 :: Machine1 -> Instr -> Machine1
update1 (mem, mask, ones) (SetMask s) = (mem, mask', ones')
    where
        mask' = interpret 'X' s
        ones' = interpret '1' s
update1 (mem, mask, ones) (Store addr value) = (mem', mask, ones)
    where
        mem' = IntMap.insert addr (value .&. mask .|. ones) mem


-- Part 2 implementation

type Machine2 = ({-mem-} IntMap Int, {-mask-} Int, {-ones-} Int, {-free-} Int)

init2 = (IntMap.empty, 0, 0, 0) :: Machine2

update2 :: Machine2 -> Instr -> Machine2
update2 (mem, mask, ones, free) (SetMask s) = (mem, mask', ones', free')
    where
        mask' = interpret '0' s
        ones' = interpret '1' s
        free' = interpret 'X' s
update2 (mem, mask, ones, free) (Store addr value) = (mem', mask, ones, free)
    where
        mem' = foldl' update mem (submasks free)
        update mem extra = IntMap.insert (addr .&. mask .|. ones .|. extra) value mem


main = do
    input <- getContents
    let instrs = map parseInstr (lines input)
    let (mem1, _, _) = foldl' update1 init1 instrs
    print $ IntMap.foldl' (+) 0 mem1
    let (mem2, _, _, _) = foldl' update2 init2 instrs
    print $ IntMap.foldl' (+) 0 mem2
