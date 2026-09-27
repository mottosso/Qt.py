#!/usr/bin/env python
import caveats


def main():
    blocks = caveats.parse("CAVEATS.md")
    tests = caveats.format_(blocks)

    # Write formatted tests
    with open("test_caveats.py", "w") as f:
        f.write("\n".join(tests).lstrip())


if __name__ == "__main__":
    main()
