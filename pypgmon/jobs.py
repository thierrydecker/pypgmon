"""Module name.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import json
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
                                    'cluster': host + ':' + str(port),
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
        print(json.dumps(points, indent=4))
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
                            schemaname,
                            relname,
                            seq_scan,
                            seq_tup_read,
                            idx_scan,
                            idx_tup_fetch,
                            n_tup_ins,
                            n_tup_upd,
                            n_tup_del,
                            n_tup_hot_upd,
                            n_live_tup,
                            n_dead_tup,
                            n_mod_since_analyze 
                        FROM
                            pg_stat_all_tables
                        """
                )
                points = []
                for row in cursor.fetchall():
                    measurement = 'pg_stat_all_tables'

                    schemaname = row[0]
                    relname = row[1]
                    seq_scan = row[2]
                    seq_tup_read = row[3]
                    idx_scan = row[4]
                    idx_tup_fetch = row[5]
                    n_tup_ins = row[6]
                    n_tup_upd = row[7]
                    n_tup_del = row[8]
                    n_tup_hot_upd = row[9]
                    n_live_tup = row[10]
                    n_dead_tup = row[11]
                    points.append(
                            {
                                'measurement': measurement,
                                'tags': {
                                    'cluster': host + ':' + str(port),
                                    'dbname': dbname,
                                    'schemaname': schemaname,
                                    'relname': relname,
                                },
                                'fields': {
                                    'seq_scan': seq_scan,
                                    'seq_tup_read': seq_tup_read,
                                    'idx_scan': idx_scan,
                                    'idx_tup_fetch': idx_tup_fetch,
                                    'n_tup_ins': n_tup_ins,
                                    'n_tup_upd': n_tup_upd,
                                    'n_tup_del': n_tup_del,
                                    'n_tup_hot_upd': n_tup_hot_upd,
                                    'n_live_tup': n_live_tup,
                                    'n_dead_tup': n_dead_tup,
                                }
                            },
                    )
        logger.debug(points)
        print(json.dumps(points, indent=4))
        logger.info(f'Database {dbname} ({description}) polled')
    except psycopg2.OperationalError as e:
        logger.error(f'Could not poll database {dbname} on {host}:{port}')
        logger.error({e})
