[Advent of Code Day 10 (Syntax Scoring) part 1 in Brainfuck

Problem description: https://adventofcode.com/2021/day/10

Minimized version:

>>>+>>>+++++>,[---------->+<[------------------------------[-[------------------
-[--[-----------------------------[--[------------------------------[[-]>->>+>++
+<<<<]>[->+>>+++<<<]<]>[->>+>++<<<]<]>[->+>>++<<<]<]>[->>+>++++<<<]<]>[->+>>++++
<<<]<]>[->>+>+<<<]<]>[->+>>+<<<]>[->>[<<<<+>>>>-]<]>[-<<<<[->+<]>>+>>>[<<<<->>+>
>-]<<<<[[-]>->[<<+>>-]<<<<[[-]>>[<+>-]<<<]>+>-[-[-[-<-<<<[<<<]>>>>+++++++>>[-]+>
+++>>[-]+>+>>[-]+>+++++>>[-]+>++>>[>>>]>]<[-<<<[<<<]>>>>+++++++>>[-]+>+++++++++>
>[-]+>+>>[-]+>+>>[>>>]]>]<[-<<<[<<<]>>>>+++++++>>[-]+>+++++>>[>>>]]>]<[-<<<[<<<]
>>>>+++>>[>>>]]<<<[<<<]>>>[>[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->+<[->[-]>
[-]>+<+<<[->+<]]]]]]]]]]]>[<+>-]>],----------[,----------]+++++>>]>[->[-]<]>]<<<
]>[-<<[[-]<]>+++++>>]<,]<[-]<<<[+++++[->++++++++<]>.[-]<<<<]++++++++++.[-]

If you're looking for a Brainfuck interpreter, check out my lightning fast
Brainfuck VM with integerated debugger, memory checker, wraparound detector,
and runtime profiler: https://github.com/maksverver/BrainfuckVM (Linux only)
]

The total sum is encoded as a list of triples: 1;d;0 where d is a decimal digit
Start with just a single 0 encoded as: 1;0;0
>>> + >>>

Following the sum is the stack which consists of positive numbers indicating
the type of bracket: 1 for parentheses; 2 for square brackets; 3 for curly
braces; 4 for angle brackets; 5 for the bottom of the stack
+++++ >

The stack will be reset whenever we find a newline or detect a mismatch

Read input one byte at a time
,[
  >+<
  Tape: stack top; (input char) 1
  ----------[  if gt 10
    Parse character and add 3 cells: 1 if open; 1 if close; bracket type
    ------------------------------[ if gt 40
      -[ if gt 41
        -------------------[ if gt 60
          --[ if gt 62
            -----------------------------[ if gt 91
              --[ if gt 93 rbracket
                ------------------------------[ if gt 123
                  [-]>-
                  125 rbrace
                  > >+ >+++ <<<
                  <
                ]>[-
                  123 lbrace
                  >+ > >+++ <<<
                ]<
              ]>[-
                93 rbracket
                > >+ >++ <<<
              ]<
            ]>[-
              91 lbracket
              >+ > >++ <<<
            ]<
          ]>[-
            62 rangle
            > >+ >++++ <<<
          ]<
        ]>[-
          60 langle
          >+ > >++++ <<<
        ]<
      ]>[-
        41 rparen
        > >+ >+ <<<
      ]<
    ]>[-
      40 lparen
      >+ > >+ <<<
    ]<

    tape: stack top; (0); 0; is_open; is_close; bracket type

    >>[-
      Opening bracket; push bracket type onto stack
      >>[-<<<<+>>>>]<<
      >
    ]>[-
      Closing bracket; compare bracket type against stack top
      tape: stack top; 0; 0; 0; (0); bracket type

      <<<<[->+<]>>>>
      <<+>>
      >[-<<+<<->>>>]< this can underflow but i'm lazy so i'll allow it

      tape: stack top; 0; diff; 1; bracket type; (0)

      <<<[
        Bracket type does not match top of stack
        tape: stack top; 0; (diff); 1; bracket type

        [-] >- >[-<<+>>]< < clean up

        tape: stack top; 0; (bracket type)

        Clear stack
        <<[
          [-]
          >>[-<+>]<<  move bracket type left
          <
        ]>>

        Add score to sum based on bracket type
        <+>-
        [-
          [-
            [-
              <-
              bracket type 4 (score 25137)
              <<<[<<<]>>>  skip to start of number
              >+++++++>>    add 7
              [-]+>+++>>    add 3
              [-]+>+>>      add 1
              [-]+>+++++>>  add 5
              [-]+>++>>     add 2
              [>>>]
              >
            ]<[-
              bracket type 3 (score 1197)
              <<<[<<<]>>>  skip to start of number
              >+++++++>>        add 7
              [-]+>+++++++++>>  add 9
              [-]+>+>>          add 1
              [-]+>+>>          add 1
              [>>>]
            ]>
          ]<[-
            bracket type 2 (score 57)
            <<<[<<<]>>>   skip to start of number
            >+++++++>>    add 7
            [-]+>+++++>>  add 5
            [>>>]
          ]>
        ]<[-
          bracket type 1 (score 3)
          <<<[<<<]>>>  skip to start of number
          >+++>>       add 3
          [>>>]
        ]

        Normalize decimal digits
        <<<[<<<]>>>
        [>
          [->+< [->+< [->+< [->+< [->+< [->+< [->+< [->+< [->+< [-
            greater than ten; reduce and carry the 1
            >[-]>[-]+>+<<<
            [->+<]
          ] ] ] ] ] ] ] ] ] ]
          >[-<+>]>
        ]
        [>>>]

        Discard input bytes until we find a newline
        ,----------[,----------]

        Reset stack to 5
        +++++
        >>
      ]>[-
        Bracket type matches top of stack (which we already cleared)
        >[-]<  delete bracket type
      ]>
    ]<<<
  ]>[-
    10 newline

    Reset stack to 5
    <<[[-]<]>+++++>>
  ]<
,]

Finally print digits while consuming them
<[-]
<<<[
  add 48 for ASCII 0
  +++++[->++++++++<]
  >.[-]<
  <<<
]

Print newline ASCII 10
++++++++++.[-]

Now the tape is cleared and the head is back to position 0
EOF
