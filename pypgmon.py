"""PyPgMon main module.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import logging
import sys

from pypgmon.helpers import check_app_conf
from pypgmon.helpers import infinite_loop
from pypgmon.helpers import parse_arguments
from pypgmon.jobs import create_scheduler


def main():
    """Entry point of the application"""
    arguments = parse_arguments()
    conf = check_app_conf(arguments=arguments, )
    if conf is None:
        sys.exit(1)
    logger = logging.getLogger('pypgmon')
    logger.info(f'Starting...')
    scheduler = create_scheduler(configuration=conf)
    if scheduler is None:
        sys.exit(1)
    scheduler.start()
    logger.info(f'Started')
    infinite_loop()
    logger.info(f'Stopping...')
    scheduler.remove_all_jobs()
    scheduler.shutdown()
    logger.info(f'Stopped')


if __name__ == '__main__':
    main()
