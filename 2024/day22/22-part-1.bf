[
    Advent of Code 2024 day 22: Monkey Market
    https://adventofcode.com/2024/day/22

    Memory layout:

    Header:

    0: 0 0 0 0     (first cell must be kept at 0)

    Current input number with 24 binary digits using 4 cells per bit:

    4: 1 b 0 0     (extra two cells are scratch space)

    Footer:

    100: 0 0 0 0

    Total in decimal digits

    104: 1 0 0 digit
]

[ Create memory layout ]

>>>++++[->++++++<]>[-[->>>>+<<<<]+>>>>]
>>>> + <<<< <<<<[<<<<]

head=0

Outer IO loop; read bytes into header: 0 char is_newline 0 

>,[
    >+<

    ----------[
        Digit; subtract 48 to convert from ASCII to value
        -->+++++[-<------>]

        Multiply each bit by 10
        >>[>[->++<]>[-<+++++>]>>]<<<<[<<<<]

        Add new digit to the least significant bit
        >[->>>>+<<<<]

        Normalize binary number
        >>>
        [
            >
            [-
                >+<
                [-
                    >-<
                    [->>+<<]
                    >>>>+<<<<
                ]
                >>[-<<+>>]<<
            ]
            block contains: 1; digit; last bit; rest; 0
            >[-<+>]>>
        ]

        >[-]< clear overflow

        <<<<[<<<<]

        >
    ]
    
    >[-
        Newline detected (head=2)

        Iterate 2000 times
        <+++++[->++++++++++<]>  50 times
        [->
            <<+++++[->>++++++++<<]>>  40 times
            [->
                STEP 1: xor register with itself left shifted by 6

                first update cells so each cell is: 1 bit_i 0 bit_i_minus_6

                [>>>>] <<<<
                <<<< <<<< <<<< <<<< <<<< <<<< [
                    >[->+<]>
                    [-<+>
                        >>>> >>>> >>>> >>>> >>>> >>>> >+<
                        <<<< <<<< <<<< <<<< <<<< <<<<
                    ]<<

                    <<<<
                ]
                >>>>
                xor bits together
                [>>>[-<+<[->-<]>[-<+>]>]>]

                at end of last bit

                STEP 2: xor register with itself right shifted by 5

                first update cells so each cell is: 1 bit_i 0 bit_i_plus_5
                <<<< [<<<<] >>>>
                >>>> >>>> >>>> >>>> >>>> [
                    >[->+<]>
                    [-<+>
                        <<<< <<<< <<<< <<<< <<<< >+<
                        >>>> >>>> >>>> >>>> >>>>
                    ]>>
                ]
                <<<< [<<<<] >>>>
                xor bits together
                [>>>[-<+<[->-<]>[-<+>]>]>]

                at end of last bit
                <<<<

                STEP 3: xor register with itself left shifted by 11
                <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< [
                    >[->+<]>
                    [-<+>
                        >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >>>> >+<
                        <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<< <<<<
                    ]<<

                    <<<<
                ]
                >>>>
                xor bits together
                [>>>[-<+<[->-<]>[-<+>]>]>]

                <<<<[<<<<]>>>>
            <]
        <]

        >>
        head=4

        [>>+>>]<<[
            [->+<]>[
                <<[->>>>+<<<<]>>
                >>>>
            ]

            now we have
                1  0  0  0 
                0  b  0 (0)
                1  0  0  0

            >

            head=104 (first decimal digit)

            double existing decimal number to be added
            [>[->+<]>[-<++>]>>]

            <<<< [<<<<] >>>>

            add bit
            <<< [->>>>+<<<<] >>>

            normalize decimal number
            [
                >
                [->+< 1
                    [->+< 2
                        [->+< 3
                            [->+< 4
                                [->+< 5
                                    [->+< 6
                                        [->+< 7
                                            [->+< 8
                                                [->+< 9
                                                    [- >[-] >>[-]+>+<<< < [->+<] ] ]
                                                ]]]]]]]]
                >[-<+>]<
                >>>
            ]
            <<<<[<<<<]<

            skip bits already processed
            [<<<<]
            <
        ]

        clear 1 digits
        > >>>> [->>>>]  >

        head=104 (first decimal digit)

        add number to total
        [> [->>+<<] >>>]
        <<<< [<<<<]

        normalize total
        >>>>
        [
            >>>
            [-<+> 1
                [-<+> 2
                    [-<+> 3
                        [-<+> 4
                            [-<+> 5
                                [-<+> 6
                                    [-<+> 7
                                        [-<+> 8
                                            [-<+> 9
                                                [- <[-]> >[-]+>>>+<<< < [-<+>] ] ]
                                            ]]]]]]]]
            <[->+<]>
            >
        ]
        <<<< [<<<<]

        head=100

        <<<< [<<<<]

        head=0

        >>
    ]<
,]<

skip past register
>>>>[>>>>]>>>>

head=104

print out total while clearing number
[>>>>]<<<<[->> ++++++[->++++++++<]>. [-] <<< <<<<]

++++++++++.[-] print newline

clear data and return head to 0 (this isn't really necessary but I like it conceptually)
<<<<[-<<<<]
