layout:

      0     1    2     3     4                5       6
    (dir) (add) (tmp)  (tmp) (val mod 100)  (tmp)     1 (dig) 1 (dig) 1 (dig) etc


init val to 50 and answer to 0
>>> +++++[->++++++++++<] >>>+<<< <<<

read dir
,[ at 0

  subtract 76 to make L 0
  +>+++++++[-<----------->]

  read last two digits
  ,----------[ at 1
    >>[-]<[->+<]          keep last digit
    ++++++[-<------>]<--  subtract 38
    [->+<] move into place
  ,----------]

  >>[-<++++++++++>]   add tens to units
  <<

  now we have dir (0) add

  <[[-]
    letter was R keep positive value
    >>[-<+>]<<
  ]
  >>[
    letter was L create 100 min units
    <<++++++++++[->++++++++++<]>>[-<->]
  ]
  <
  now at cell 1 which contains the value to add

  subtract one by one from val mod 100
  [-
    >>+>[-[->+<]<[-]>]   subtract 1 if we can
    <[-+++++++++[->>+++++++++++<<]] otherwise add 99
    >>[-<+>]<<<<
  ]

  check if val is 0
  >+>>[-<+>]<[<->[->+<]]<

  at cell 2
  [-
    add 1 to answer

    >>>>>+<[-
      >[-<+>]<
      [->+< [->+< [->+< [->+< [->+< [->+< [->+< [->+< [->+< [
        ->[-]>[-]+>+<<<
      ] ] ] ] ] ] ] ] ] ]
      +>>
    ]
    <<[<<]<<
  ]

  back to 0 and read next char
  << ,
]

>>>>[-]  delete val

print out answer
>>[>>]<<[
  +++++[->++++++++<] add 48
  >.[-]<<<
]

++++++++++.  print newline
