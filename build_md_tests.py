#!/usr/bin/env python
import os
import mdparse

# Test caveats
blocks = mdparse.parse("CAVEATS.md")
tests = mdparse.format_(blocks)
with open("test_caveats.py", "w") as f:
    f.write("".join(tests))

# Test examples
for example in os.listdir('examples'):
    blocks = mdparse.parse(os.path.join('examples', example))
    tests = mdparse.format_(blocks)
    with open("test_examples.py", "w+") as f:
        f.write("".join(tests))
