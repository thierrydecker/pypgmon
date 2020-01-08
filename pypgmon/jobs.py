"""Module name.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import logging

import psycopg2


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
        cluster: Cluster's key
        description: Cluster's description
        host: Cluster's hostname or ip address
        port:Cluster's port
        dbname: Cluster's dbname
        user: Cluster's user
        password: Cluster's user password

    Returns:

    Raises:

    """
    logger = logging.getLogger(__name__)
    logger.debug(f'Polling cluster {cluster} ({description})...')
    conn = None
    try:
        conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password,
        )
        conn.close()
        logger.info(f'Cluster {cluster} ({description}) polled')
    except psycopg2.OperationalError as e:
        logger.error(f'Could not poll cluster {host}:{port}')
        logger.error({e})


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
    conn = None
    try:
        conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password,
        )
        conn.close()
        logger.info(f'Database {database} ({description}) polled')
    except psycopg2.OperationalError as e:
        logger.error(f'Could not poll database {host}:{port}')
        logger.error({e})
