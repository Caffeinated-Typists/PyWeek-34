import sys
import subprocess

# The major, minor version numbers your require
MIN_VER = (3, 10)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )

subprocess.run("python Project-Aries")
