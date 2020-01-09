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
    try:
        with psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                        """
                        SELECT
                            datname,
                            numbackends,
                            xact_commit,
                            xact_rollback,
                            blks_read,
                            blks_hit,
                            tup_returned,
                            tup_fetched,
                            tup_inserted,
                            tup_updated,
                            tup_deleted,
                            conflicts,
                            temp_files,
                            temp_bytes,
                            deadlocks,
                            blk_read_time,
                            blk_write_time 
                        FROM
                            pg_stat_database
                        """
                )
                points = []
                for row in cursor.fetchall():
                    measurement = 'pg_stat_database'
                    datname = row[0]
                    numbackends = row[1]
                    xact_commit = row[2]
                    xact_rollback = row[3]
                    blks_read = row[4]
                    blks_hit = row[5]
                    tup_returned = row[6]
                    tup_fetched = row[7]
                    tup_inserted = row[8]
                    tup_updated = row[9]
                    tup_deleted = row[10]
                    conflicts = row[11]
                    temp_files = row[12]
                    temp_bytes = row[13]
                    deadlocks = row[14]
                    blk_read_time = row[15]
                    blk_write_time = row[16]
                    points.append(
                            {
                                'measurement': measurement,
                                'tags': {
                                    'cluster': cluster + ':' + str(port),
                                    'datname': datname,
                                },
                                'fields': {
                                    'numbackends': numbackends,
                                    'xact_commit': xact_commit,
                                    'xact_rollback': xact_rollback,
                                    'blks_read': blks_read,
                                    'blks_hit': blks_hit,
                                    'tup_returned': tup_returned,
                                    'tup_fetched': tup_fetched,
                                    'tup_inserted': tup_inserted,
                                    'tup_updated': tup_updated,
                                    'tup_deleted': tup_deleted,
                                    'conflicts': conflicts,
                                    'temp_files': temp_files,
                                    'temp_bytes': temp_bytes,
                                    'deadlocks': deadlocks,
                                    'blk_read_time': blk_read_time,
                                    'blk_write_time': blk_write_time,
                                }
                            },
                    )
        logger.debug(points)
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
