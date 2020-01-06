"""Module name.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import pg_stat_all_tables
from .jobs import pg_stat_database


def create_scheduler(conf):
    """Start scheduler

    Args:
        conf: A valid configuration dictionnary

    Returns:
        A scheduler or None

    Raises:

    """
    logger = logging.getLogger(__name__)
    try:
        max_workers = conf['scheduler']['max_workers']
        scheduler = BackgroundScheduler(
                executors={
                    'default':
                        {
                            'type': 'threadpool',
                            'max_workers': max_workers,
                        },
                }
        )
        logger.info(f'Scheduler created for {max_workers} workers')
        logger.info(f'Adding clusters targets...')
        for cluster in conf['clusters']:
            description = conf['clusters'][cluster]['description']
            host = conf['clusters'][cluster]['host']
            port = conf['clusters'][cluster]['port']
            dbname = conf['clusters'][cluster]['dbname']
            user = conf['clusters'][cluster]['user']
            password = conf['clusters'][cluster]['password']
            seconds = conf['clusters'][cluster]['interval']
            scheduler.add_job(
                    pg_stat_database,
                    'interval',
                    kwargs={
                        'cluster': cluster,
                        'description': description,
                        'host': host,
                        'port': port,
                        'dbname': dbname,
                        'user': user,
                        'password': password,
                    },
                    name=cluster,
                    seconds=seconds,
            )
            logger.info(f'Cluster target {cluster} added')
        logger.info(f'Clusters targets added')
        logger.info(f'Adding databases targets...')
        for database in conf['databases']:
            description = conf['databases'][database]['description']
            host = conf['databases'][database]['host']
            port = conf['databases'][database]['port']
            dbname = conf['databases'][database]['dbname']
            user = conf['databases'][database]['user']
            password = conf['databases'][database]['password']
            seconds = conf['databases'][database]['interval']
            scheduler.add_job(
                    pg_stat_all_tables,
                    'interval',
                    kwargs={
                        'database': database,
                        'description': description,
                        'host': host,
                        'port': port,
                        'dbname': dbname,
                        'user': user,
                        'password': password,
                    },
                    name=database,
                    seconds=seconds,
            )
            logger.info(f'Database target {database} added')
        logger.info(f'Databases targets added')
    except ValueError as e:
        logger = logging.getLogger(__name__)
        scheduler = None
        logger.error(f'Creating the scheduler, {e}')
    return scheduler
