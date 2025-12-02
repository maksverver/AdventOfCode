[
Advent of Code 2025 day 1 part 2 in Brainfuck

Works for arbitrarily large inputs also with more than 3 digits per command

See bf-logic-part-2-method-2.py for an explanation how this works
Essentially I divide every number in the input by 100 and handle the quotient
and remainder separately

Memory layout:

0 is_L tmp tmp 1 dig tmp 1 dig tmp 1 dig tmp

where dig are digits in base 10 in least significant decimal order
and tmp is temporary space that is reset to 0
]

>
>>> +> >> +>+++++> >+ <<< <<< <<<

,[

  detect L
  +>+++++++[-<----------->]+<[[-]>-<]

  now tape is: (zero) is_L zero

  BEGIN OF BLOCK COPIED BELOW
  >[->+<
    if L

    >>> >>>

    invert tens digit
    [>++++++++++<[->-<]]>[-<+>]<

    invert unit digit
    <<<
    [
      borrow 1 from tens
      >>>
      [->+<]
      +++++++++
      >[-<[-]>[-<+>]]<
      <<<
      >++++++++++<[->-<]
    ]
    >[-<+>]<

    <<<
  ] at 2
  END OF BLOCK COPIED BELOW

  >[-<+>]<
  now tape is: zero (is_L) zero

  >

  read digits
  ,----------[--
    move existing digits back
    >>>[>>>] <<[-]+<
    [[->>>+<<<]<<<]>>>
  ,----------]

  add digits into total
  >>>[>>>]<<<[
    [-<+>]
    ++++++[-<------>] subtract 36
  <<<]

  normalize digits in answer from digit 3 on because digit 1 and 2 are known zero
  >[
    >[->+<]> copy
    [-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-<+>[-
      >[-]+>+<<   create next digit if needed and add carry
      <[-]>[-<+>] move remainder
    ] ] ] ] ] ] ] ] ] ]
    >
  ]
  <<<[<<<]

  BEGIN OF BLOCK COPIED ABOVE
  >[-     EXCEPTION dont keep this bit
    if L

    >>> >>>

    invert tens digit
    [>++++++++++<[->-<]]>[-<+>]<

    invert unit digit
    <<<
    [
      borrow 1 from tens
      >>>
      [->+<]
      +++++++++
      >[-<[-]>[-<+>]]<
      <<<
      >++++++++++<[->-<]
    ]
    >[-<+>]<

    <<<
  ] at 2
  END OF BLOCK COPIED ABOVE
  <

,]

print out answer from digit 3 on
>>> - >>> - >>>

[>>>]<<<[
  +++++[->++++++++<] add 48
  >.[-]<
  <<<
]

++++++++++.  print newline
