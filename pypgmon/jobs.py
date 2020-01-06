"""Module name.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import logging
import random
import time


def pg_stat_database(
        cluster,
        description,
        host,
        port,
        dbname,
        user,
        password,
):
    """pg_stat_database job

    Args:
        cluster:
        description:
        host:
        port:
        dbname:
        user:
        password:

    Returns:

    Raises:

    """
    logger = logging.getLogger(__name__)
    logger.debug(f'Polling cluster {cluster} ({description})...')
    time.sleep(random.randint(0, 4))
    logger.info(f'Cluster {cluster} ({description}) polled')


def pg_stat_all_tables(
        database,
        description,
        host,
        port,
        dbname,
        user,
        password,
):
    """pg_stat_all_tables job

    Args:
        database:
        description:
        host:
        port:
        dbname:
        user:
        password:

    Returns:

    Raises:

    """
    logger = logging.getLogger(__name__)
    logger.debug(f'Polling database {database} ({description})...')
    time.sleep(random.randint(0, 4))
    logger.info(f'Database {database} ({description}) polled')
