"""Module name.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler


def create_scheduler(configuration):
    """Start scheduler

    Args:
        configuration: A valid configuration dictionnary

    Returns:
        A scheduler or None

    Raises:

    """
    try:
        max_workers = configuration['scheduler']['max_workers']
        scheduler = BackgroundScheduler(
                executors={
                    'default':
                        {
                            'type': 'threadpool',
                            'max_workers': max_workers,
                        },
                }
        )
        logger = logging.getLogger(__name__)
        logger.info(f'Scheduler created for {max_workers} workers')
    except ValueError as e:
        scheduler = None
        logger = logging.getLogger(__name__)
        logger.error(f'Creating the scheduler, {e}')
    return scheduler
