[ Advent of Code 2024 day 22: Monkey Market
https://adventofcode.com/2024/day/22

Solution written in standard Brainfuck.

At a high level, the program does the following:

1) For each number in the input:

    a) convert the number to a 24 bit binary representation
    b) apply the hash function 2000 times
    c) add the final value to the total

2) At the end of the input, print the total (the puzzle solution)

The hash function boils down to:

    x = (x ^ (x <<  6)) & 0xffffff
    x = (x ^ (x >>  5)) & 0xffffff
    x = (x ^ (x << 11)) & 0xffffff

with ^ as bitwise XOR, << and >> as left and right shift, and & bitwise AND.
Clearly this is easiest to implement in binary rather than decimal, so when
we read numbers, we convert them to binary, using a fixed 24-bit register.
If we discard any overflow we don't even need to implement the AND operation
explicitly.

On a lower level, step 1 looks as follows:

    Start with the register containg all 0 bits

    When we read a digit:

        a) multiply the register by 10
        b) add the new digit to the register

    When we read a newline:

        execute steps 1b and 1c
        (step 1c clear the register for the next number as a side effect)

Note that we never read all the input numbers into memory at once. We don't
even load a single number, at least not in decimal: every decimal digit that
comes in is immediately converted to binary.

Step 2c adds the 24-bit result to the total, which will contain our final
answer. Of course, this answer needs to be printed in decimal. To avoid having
to convert a large binary number to decimal, I keep the total (our answer)
in decimal. That means that after applying the hash function 2000 times, the
result must be converted to decimal, which I do by a combination of doubling
and adding.

So step 2c looks something like:

    - Start with the decimal number 0
    - While there are bits left in the register:
        - Double the decimal number
        - Take the most significant bit in the register
        - Add it to the decimal number
    - Add the decimal result to the decimal total

The doubling and adding happens in decimal. This way, the total is always in
decimal and no tricky division operations are necessary to print out the answer
at the end.

Now that the high level logic is explained, we can discuss the memory
representation. I use 4 cells per bit for the 24-bit register, and another
4 cells per decimal digit, which gives me plenty of scratch space to work with.

In more detail:

    header (4 cells)
    0: 0 0 0 0    first cell must always be 0; others are used to read input


    24 bit register (4 * 24 = 96 cells)

    4: 1 b 0 0     first cells are 1 to enable navigating front to back
    8: 1 b 0 0     second cells contain bits (least significant first)
  ...              third and fourth cells are scratch space (normally 0)
   96: 1 b 0 0

    footer (4 cells)

 100: 0 0 0 0      first cell must be zero; others are used as scratch space

    decimal number (4 * x cells; x=1 initiall by may expand to however many
                    decimal digits we need)

 104: 1 0 0 d       first cells are always 1 to enable navigating front to back
                    second cells contain the register value in decimal before
                            being added (they're otherwise zero)
                    third cells are used as scratch space
                    fourth cells contain the total in decimal

Note: in theory it might have been possible to use only 3 cells for either
the decimal total or the binary register or both, but I'm too lazy to change it
now that the program works.
]

Start by creating the memory layout described above with 24 1 bits to mark
the 24 bit register and 1 bit for the total which starts at 0
>>>++++[->++++++<]>[-[->>>>+<<<<]+>>>>]
>>>> + <<<< <<<<[<<<<]

Outer IO loop; read bytes into cell 1
>,[
    Create a boolean in cell 2 that indicates whether the current character
    is a newline or not
    >+<

    Here we have: 0 (ch) is_nl 0

    ----------[
        Digit; subtract 48 to convert from ASCII to value
        -->+++++[-<------>]

        Multiply the existing bits in the register by 10
        >>[>[->++<]>[-<+++++>]>>]<<<<[<<<<]

        Add the new digit to the least significant bit
        >[->>>>+<<<<]

        Now each "bit" actually contains a number between 0 and 19 inclusive;
        so we must normalize the binary digits to 0 or 1 making sure to carry
        correctly.
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
            >[-<+>]>>
        ]

        We are now at the end of the number; if we overflowed the carry ended
        up here and we'll just clear it since we are doing 24 bit arithmetic
        >[-]<

        Move back to the front of the number
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
                then xor bits together
                [>>>[-<+<[->-<]>[-<+>]>]>]
                at the end of the last bit (head=100)
                <<<<

                STEP 2: xor register with itself right shifted by 5

                first update cells so each cell is: 1 bit_i 0 bit_i_plus_5
                [<<<<] >>>>
                >>>> >>>> >>>> >>>> >>>> [
                    >[->+<]>
                    [-<+>
                        <<<< <<<< <<<< <<<< <<<< >+<
                        >>>> >>>> >>>> >>>> >>>>
                    ]>>
                ]
                <<<< [<<<<] >>>>
                then xor bits together
                [>>>[-<+<[->-<]>[-<+>]>]>]
                at the end of the last bit (head=100)
                <<<<

                STEP 3: xor register with itself left shifted by 11

                first update cells so each cell is: 1 bit_i 0 bit_i_minus_11
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
                at the end of the last bit (head=100)
                move back to the front
                <<<<[<<<<]>>>>
            <]
        <]

        >>
        (head=4)

        We are the start of the first bit in the register which contains the
        value to be converted to decimal and added to the total

        We will use cells three and four of each block to indicate whether a
        bit has not been added or has been added

        For example we start with

            1 a 1 0
            1 b 1 0
            1 c 1 0
            1 d 1 0
            0 0 0 0

        Then we take the most significant bit and move it down to the footer
        just above the start of the decimal total:

            1 a 1 0
            1 b 1 0
            1 c 1 0
            1 0 0 1
            0 d 0 0

        Then after we add in d we take the next bit:

            1 a 1 0
            1 b 1 0
            1 0 0 1
            1 0 0 1
            0 c 0 0

        And so on;

        First mark all the third cells 1
        [>>+>>]<<

        (head=98; at the third cell of the last register block)

        This loop will convert the binary bits to a decimal number
        one at a time; from most to least significant
        [
            Move the 1 from cell 3 to cell 4 to indicate this bit has been
            processed (or; will be soon enough)
            [->+<]>

            Move the bit down to the footer
            [<<[->>>>+<<<<]>> >>>>]

            >
            Now we are at the footer where we have the decimal total
            in the fourth column and we will first construct the registers
            decimal value

               0  b  0 (0)
              (1) 0  0  d
               1  0  0  d

            (head=104; at the first decimal digit)

            Double existing decimal number
            [>[->+<]>[-<++>]>>] <<<< [<<<<] >>>>

            Add bit from footer to decimal number
            <<< [->>>>+<<<<] >>>

            Normalize the decimal number
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

            Move back up using the fourth column to skip bits that have already
            been processed
            [<<<<]
            <
        ]

        (head at cell 2)

        Clear the 1 digits that are now all in column 4
        > >>>> [->>>>] >

        head=104 (first decimal digit)

        We add the decimal result (in column 1) to the decimal total (in column 4)
        [> [->>+<<] >>>]
        <<<< [<<<<]

        Normalize the decimal total which may now contain digits up to 19
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

        Move head all the way back to the start
        <<<< [<<<<] (head=100) <<<< [<<<<] (head=0)

        >>
    ]<
,]<

Finally we are done processing all the input and we have the answer ready in
decimal and waiting to be printed

Skip past register
>>>>[>>>>]>>>>
(head=104)

Print out total while clearing number
[>>>>]<<<<[->> ++++++[->++++++++<]>. [-] <<< <<<<]

Print a final newline character
++++++++++.[-]

Clear data and return head to 0 (this isn't really necessary but I like the
idea of cleaning up after myself)
<<<<[-<<<<]
