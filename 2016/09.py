import re
import sys

def GetOutputLength(data, begin, end, recurse):
  pattern = re.compile(r'\((\d+)x(\d+)\)')
  output_length = 0
  while True:
    match = pattern.search(data, begin, end)
    if match:
      #                     match.    match.
      #   begin             start(0)  end(0)             suffix_end
      #     |                 |        |                 |
      #     |<-prefix_length->|        |<-suffix_length->|
      #     v                 v        v                 v
      #  ...PrefixDataGoesHere(123x456)SuffixDataGoesHere...
      #
      prefix_length = match.start(0) - begin
      suffix_length, num_copies = map(int, match.groups())
      suffix_begin = match.end(0)
      suffix_end = suffix_begin + suffix_length
      if recurse:
        copy_length = GetOutputLength(data, suffix_begin, suffix_end, True)
      else:
        copy_length = suffix_length
      output_length += prefix_length + num_copies*copy_length
      begin = suffix_end
    else:
      return output_length + end - begin

data = sys.stdin.read().strip()
print(GetOutputLength(data, 0, len(data), recurse=False))
print(GetOutputLength(data, 0, len(data), recurse=True))
