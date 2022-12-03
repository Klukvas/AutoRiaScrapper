import sys
from os import getenv

from CarChooser.Scrapper.AutoRia import ria_parser
from CarChooser.Scrapper.query import Query
from CarChooser.Scrapper.serializer import Serializer
from CarChooser.Configs.logger import Logger

from CarChooser.RestApi import api_runner
from CarChooser.Scrapper.utils import files_utils

from CarChooser.Configs.config_utils import get_config, Config_env, Config_type

AVAILABLE_START_ARGS = ["autoria", "runserver"]

def _prepare_alembic_config() -> None:
    #find path tp alembic.ini file
    path_to_configs = str(files_utils.find_file('alembic.ini'))
    # find path to migrations folder
    path_to_migration_folder = str(files_utils.find_file('migrations', False))
    # change paths in alembic.ini file
    files_utils.change_alembic_ini(path_to_configs, path_to_migration_folder)
    return


def start():
    argument_list = sys.argv[1:]
    log = Logger().custom_logger('CarParserLog')

    if argument_list:
        # to success functionality alembic need to know where is alembic.ini file located
        _prepare_alembic_config()

        query = Query(log)
        serializer = Serializer(log)
        for argument in argument_list:
            if argument == 'autoria':
                scrapper_config = get_config(
                    Config_type.SCRAPPER.value,
                    Config_env[getenv('FLASK_ENV', 'development')].value
                )
                
                ria_parser.run(
                        log, 
                        scrapper_config.AUTO_RIA_API_KEYS,
                        scrapper_config.MAX_PULL,
                        query, 
                        serializer
                    )
            elif argument == 'runserver':
                api_runner.runserver()
            else:
                log.error(f"Can not find your argument: {argument}\nAvailable args: {AVAILABLE_START_ARGS}")
    else:
        log.error(f'With run command u must to pass the one of arguments: {AVAILABLE_START_ARGS}')


if __name__ == '__main__':
    start()
    