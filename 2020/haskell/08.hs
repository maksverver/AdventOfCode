import Data.Array
import Deque (Deque)
import qualified Deque
import Data.IntSet (IntSet)
import qualified Data.IntSet as IntSet

data Instruction = Nop Int | Acc Int | Jmp Int deriving Show

type Program = Array Int Instruction

parseInstruction :: String -> Instruction
parseInstruction s = parse (words s)
    where
        parse ["nop", i] = Nop (readInt i)
        parse ["acc", i] = Acc (readInt i)
        parse ["jmp", i] = Jmp (readInt i)
        parse _ = error s

        readInt :: String -> Int
        readInt ('+':s) = read s
        readInt s = read s

part1 :: Program -> Int
part1 program = search 0 0 IntSet.empty
    where
        search ip acc visited
            | IntSet.member ip visited = acc
            | otherwise                = search ip' acc' visited'
            where
                instr    = program ! ip
                visited' = IntSet.insert ip visited
                acc'     = case instr of Acc i -> acc + i; _ -> acc
                ip'      = case instr of Jmp i -> ip + i; _ -> ip + 1

part2 :: Program -> Int
part2 program = search (Deque.fromList [(0, 0)]) IntSet.empty
    where
        -- Finds the shortest path in a graph with binary-weighted edges,
        -- using a variant of breadth first search using a deque.
        search :: Deque (Int, Int) -> IntSet -> Int
        search todo visited
            | IntSet.member ip visited = search todo' visited
            | ip == end                = acc
            | otherwise                = search todo'' (IntSet.insert ip visited)
            where
                ((ip, acc), todo') = Deque.removeFront todo
                instr  = program ! ip
                todo'' =
                    case instr of
                        Acc i -> Deque.addFront (ip + 1, acc + i) todo
                        Nop i -> Deque.addFront (ip + 1, acc) $ Deque.addBack (ip + i, acc) todo
                        Jmp i -> Deque.addFront (ip + i, acc) $ Deque.addBack (ip + 1, acc) todo

        end = let (_, i) = bounds program in i + 1

main = do
    input <- getContents
    let instructions = map parseInstruction (lines input)
    let program = listArray (0, length instructions - 1) instructions
    print $ part1 program
    print $ part2 program
