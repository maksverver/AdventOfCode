#!/usr/bin/sed -f

1i\
digraph {

s/^%\([a-z]*\)/\1 [shape=box style=filled fillcolor=lightblue] \1/
s/^&\([a-z]*\)/\1 [shape=diamond style=filled fillcolor=lightpink] \1/

$a\
}
