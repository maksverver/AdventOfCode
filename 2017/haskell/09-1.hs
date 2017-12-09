data State = State{
    depth :: Int,
    inGarbage :: Bool,
    inEscape :: Bool,
    score :: Int,
    garbage :: Int} deriving Show

initialState = State{
    depth = 0,
    inGarbage = False,
    inEscape = False,
    score = 0,
    garbage = 0}

process :: State -> Char -> State
process state@State{inEscape = True} _ = state{inEscape = False}
process state@State{inGarbage = True} ch = process ch
    where
        process '!' = state{inEscape = True}
        process '>' = state{inGarbage = False}
        process _ = state{garbage = garbage state + 1}
process state ch = process ch
    where
        process '<' = state{inGarbage = True}
        process '{' = state{depth = new_depth, score = new_score}
            where
                new_depth = depth state + 1
                new_score = score state + new_depth
        process '}' = state{depth = depth state - 1}
        process _ = state

main = do
    input <- getLine
    let state = foldl process initialState input
    print $ score state
    print $ garbage state
