#!/usr/bin/env python
import caveats

blocks = caveats.parse("CAVEATS.md")
tests = caveats.format_(blocks)

# Write formatted tests
with open("test_caveats.py", "w") as f:
    f.write("".join(tests))
