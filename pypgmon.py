"""PyPgMon main module.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import sys

from pypgmon.helpers import conf_app


def main():
    """Entry point of the application"""
    if not conf_app():
        sys.exit(1)


if __name__ == '__main__':
    main()
