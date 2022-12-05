[ Advent of Code 2022 Day 2: Rock Paper Scissors (part 1)
https://adventofcode.com/2022/day/2

Solution in standard Brainfuck (no 8 bit cells, no wraparound)

Minimized representation:

>,[-<++++++++[->--------<]>>,,>++++++++[<----------->-]<<[->+++<]>>++++<[->++++<
[->-----<[->--<[->++++<[->++++<[->--<[->-----<[->++++<]]]]]]]]>[>>[-]+<<[->+<]>[
<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[>>+<<-<[-]>[<+>-]]]]]]]]]]]<[->+<]>
>>]<[<<<]<,[-],]>>>>[>>>]<<<[+++++[<++++++++>-]<.<<]++++++++++.

Valuation matrix

     X Y Z
     r p s

A r  4 8 3
B p  1 5 9
C s  7 2 6

Array:  4  8  3  1  5  9  7  2  6
Delta:  4  4 -5 -2  4  4 -2 -5  4

      0 1 2 3 4 5 6 7 8 9
Tape: 0 i j s a 1 0 b 1 0 c 1

i is move for player 1
j is move for player 2
s is score for this round
point total is stored in decimal digits a b c etc
]

read A/B/C into cell 1
>,[

  -<++++++++[->--------<]> sub 65 (A)
  >
    , skip space
    , read X/Y/Z

    >++++++++[-<----------->]< sub 88 (X)

    <[->+++<]>  add 3 times p1 to p2

    0 0 0 (3 times p1 plus p2)

    Calculate score from this round
    >++++<  plus 4
    [->++++<  plus 4 is 8
      [->-----<  minus 5 is 3
        [->--<   minus 2 is 1
          [->++++<  plus 4 is 5
            [->++++<  plus 4 is 9
              [->--<  minus 2 is 7
                [->-----<  minus 5 is 2
                  [->++++< plus 4 is 6
    ] ] ] ] ] ] ] ]

    Addition
    >[
      (a) d (0/1)
      >>[-]+<<    mark current digit used (needed to print later)
      [->+<]>     0 (a plus d) 1
      [-<+>
        [-<+>
          [-<+>
            [-<+>
              [-<+>
                [-<+>
                  [-<+>
                    [-<+>
                      [-<+>
                        [-              digit is greater than 10
                           >>+<<        add 1 to next digit
                           <[-]>[-<+>]  keep remainder of current digit
      ] ] ] ] ] ] ] ] ] ]
      <[->+<]>
      >> move to next digit
    ]<

  [<<<] move before digits

  at cell 2
  < at
  , skip newline
  [-]
  , read A/B/C into cell 1
]

Move to last digit
>>>>[>>>]<<<

[ 0 d 1
  +++++[-<++++++++>] convert to ASCII
  <.    write char
  <<    to previous digit
]

++++++++++.
Write newline
