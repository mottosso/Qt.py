#!/usr/bin/env python
import parser

blocks = parser.parse("CAVEATS.md")
tests = parser.format_(blocks)

# Write formatted tests
with open("test_caveats.py", "w") as f:
    f.write("".join(tests))
