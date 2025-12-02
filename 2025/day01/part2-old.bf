[
Advent of Code 2025 day 1 part 2 in Brainfuck

Works for arbitrarily large inputs also with more than 3 digits per command

Not quite minimal (I think I can remove cell 3 and/or 4 if I'm clever)
but good enough

See bf-logic-part-2.py for an explanation how this works
Essentially I divide every number in the input by 100 and handle the quotient
and remainder separately

Memory layout:

    0               1      2      3   4   5  6    7  8  9   10 11 12   13 14
    (pos mod 100)   (dir)  (tmp)  0   0   0  1 (dig) 0  1 (dig) 0  1 (dig) 0 etc
]

init total to 50 and answer to 0
>+++++[-<++++++++++>] >>>>> + >>> + >>> + <<< <<< <<< <<

read dir in cell 1
,[ at 1

  subtract 76 to make L 0
  +>+++++++[-<----------->]

  read digits
  >>> at cell 5 (cell 3 needs to be zero)
  ,----------[--
    move existing digits back
    >>>[>>>] <<[-]+<
    [[->>>+<<<]<<<]>>>
  ,----------]

  add digits into total; don't normalize now we will do this later
  >>>[>>>]<<<[
    [-<+>]
    ++++++[-<------>] subtract 36
  <<<]

  at 5

  get value modulo 100
  >>[-<<+>>]                 units
  >>> [-<< <<< ++++++++++ >>> >>]  tens
  <<< <<

  <<<< at 1
  which is nonzero if char was R
  set cell 3 and 4 to 1 if char was L
  >>+>+<<< [[-]>>->-<<<]

  >>[-  if L then invert
    <<<
      set pos = 100 min pos if pos is nonzero using temp cells 1 and 2
      NOTE this is copied below
      [
        >>++++++++++[-<++++++++++>]<< init 100
        [->-<]                        subtract pos
      ]
      >[-<+>]<                        move result back to cell 0
    >>>
  ]<<

  >>>> at 5

  here we have the current value to add to pos in cell 5
  update pos in cell 0 one step at a time using temp cells 1 and 2

  [-<<<<<
    >>+<<
    [->+<] move pos to cell 1
    >[
      nonzero: subtract 1
      -
      move back
      [-<+>>-<[-<+>]]
      >[- pos is now 0 so increment third digit of answer
          >>>>> >>> >>> + <<< <<< <<<<<
      ]<
    ] at 1
    >[-<+++++++++[-<+++++++++++>]>]  zero: assign 99
    >>> at 5
  ] at 5

  <<<< at 1

  >>>[-  if L then invert

    <<<<
      set pos = 100 min pos if pos is nonzero using 1 and 2 as temp
      NOTE this is copied from above
      [
        >>++++++++++[-<++++++++++>]<< init 100
        [->-<]                        subtract pos
      ]
      >[-<+>]<                        move result back to cell 0
    >>>>

  ]<<<

  at cell 1
  normalize digits in answer from digit 3 on because digit 1 and 2 are known zero
  >>> >>>
  >>>>>[
    >[->+<]> copy
    [-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-
      >[-]+>+<<   create next digit if needed and add carry
      <[-]>[-<+>] move remainder
    ] ] ] ] ] ] ] ] ] ]
    >
  ]
  <<<[<<<]<<
  back to cell 1

read next dir
,]

print out answer from digit 3 on
>>>>> - >>> - >>>
[>>>]<<<[
  +++++[->++++++++<] add 48
  >.[-]<
  <<<
]

++++++++++.  print newline
