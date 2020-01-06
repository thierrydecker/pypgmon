"""Helpers module.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import argparse
import logging
import logging.config
import time

import yaml
import yaml.parser
import yaml.scanner


def parse_arguments():
    """Parse command line arguments

    Args:

    Returns:
        Command line arguments

    Raises:

    """
    parser = argparse.ArgumentParser(
            prog='pypgmon',
    )
    parser.add_argument(
            '-l',
            '--logger',
            default='pypgmon/conf/logger.yml',
    )
    parser.add_argument(
            '-t',
            '--targets',
            default='pypgmon/conf/targets.yml',
    )
    arguments = parser.parse_args()
    return arguments


def conf_basic_logging():
    """Basic logging configuration

    Args:

    Returns:
        True

    Raises:

    """
    logging.basicConfig(
            filename='pypgmon/log/pypgmon.error',
            filemode='w',
            level=logging.DEBUG,
            format='%(asctime)s - '
                   '%(levelname)8s - '
                   '%(name)s - '
                   '%(message)s'
    )
    return True


def conf_logging(file_name):
    """Application logging configuration

    Args:
        file_name: A Yaml logger configuration file name

    Returns:
        True if configuration can be done
        False if configuration can NOT be done

    Raises:

    """
    try:
        with open(file_name) as f:
            conf = f.read()
        logging.config.dictConfig(yaml.safe_load(conf))
        logger = logging.getLogger(__name__)
        logger.info(f'Logger sucessfully configured')
        ok = True
    except (FileNotFoundError, ValueError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f'Logger configuration failed. {e}')
        ok = False
    return ok


def check_targets(conf):
    """Ckeck application targets configuration

    Args:
        conf: A dictonnary of targets configuration

    Returns:

    Raises:
        ValueError

    """
    #
    # Scheduler
    #
    try:
        logger = logging.getLogger(__name__)
        scheduler = conf['scheduler']
        scheduler_max_workers = scheduler['max_workers']
    except KeyError as e:
        logger = logging.getLogger(__name__)
        logger.error(f'{e} key not found in configuration')
        raise ValueError
    #
    # Clusters
    #
    try:
        clusters = conf['clusters']
        for cluster in clusters:
            k = 'description'
            v = clusters[cluster][k]
            k = 'host'
            v = clusters[cluster][k]
            k = 'port'
            v = int(clusters[cluster][k])
            k = 'dbname'
            v = clusters[cluster][k]
            k = 'user'
            v = clusters[cluster][k]
            k = 'password'
            v = clusters[cluster][k]
            k = 'interval'
            v = int(clusters[cluster][k])
    except KeyError:
        logger = logging.getLogger(__name__)
        logger.error(f'{k} key not found in cluster {cluster} configuration')
        raise ValueError
    except ValueError:
        logger = logging.getLogger(__name__)
        logger.error(f'invalid {k} key in cluster {cluster} configuration')
        raise ValueError
    #
    # Databases
    #
    try:
        databases = conf['databases']
        for database in databases:
            k = 'description'
            v = databases[database][k]
            k = 'host'
            v = databases[database][k]
            k = 'port'
            v = int(databases[database][k])
            k = 'dbname'
            v = databases[database][k]
            k = 'user'
            v = databases[database][k]
            k = 'password'
            v = databases[database][k]
            k = 'interval'
            v = int(databases[database][k])
    except KeyError:
        logger = logging.getLogger(__name__)
        logger.error(f'{k} key not found in database {database} configuration')
        raise ValueError
    except ValueError:
        logger = logging.getLogger(__name__)
        logger.error(f'invalid {k} key in database {database} configuration')
        raise ValueError


def check_targets_conf(file_name):
    """Application targets configuration

    Args:
        file_name: A Yaml targets configuration file name

    Returns:
        False if targets configuration is NOT valid
        A valid dictionary of the targets confguration

    Raises:

    """
    try:
        with open(file_name) as f:
            conf = yaml.safe_load(f.read())
        check_targets(conf=conf)
        logger = logging.getLogger(__name__)
        logger.info(f'Targets sucessfully configured')
    except FileNotFoundError:
        conf = None
        logger = logging.getLogger(__name__)
        logger.error(f'Could not find {file_name} configuration file!')
    except yaml.parser.ParserError as e:
        conf = None
        logger = logging.getLogger(__name__)
        logger.error(f'Parsing: {file_name}')
        logger.error(f'Parsing: {e.problem}')
        logger.error(f'Parsing: {e.problem_mark}')
    except yaml.scanner.ScannerError as e:
        conf = None
        logger = logging.getLogger(__name__)
        logger.error(f'Scanning: {file_name}')
        logger.error(f'Scanning: {e.problem}')
        logger.error(f'Scanning: {e.problem_mark}')
    except ValueError:
        conf = None
        logger = logging.getLogger(__name__)
        logger.error(f'Checking {file_name} sanity')
    return conf


def check_app_conf(arguments):
    """PyPgMon application configuration check

    Args:
        arguments: Command line arguments

    Returns:
        A valid targets configuration if configuration sanity passed
        None if configuration sanity failed

    Raises:

    """
    ok = True
    conf = None
    if ok and not conf_basic_logging():
        ok = False
    if ok and not conf_logging(file_name=arguments.logger):
        ok = False
    if ok:
        conf = check_targets_conf(file_name=arguments.targets)
        if conf is None:
            ok = False
    return conf


def infinite_loop():
    """Infinite loop waiting for keyboard interruption"""
    while True:
        logger = logging.getLogger(__name__)
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info(f'Stopping...')
            break
