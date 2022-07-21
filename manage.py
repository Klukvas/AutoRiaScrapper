print('asd1')
import sys

from CarChooser.Scrapper.AutoRia import ria_parser
from CarChooser.Scrapper.query import Query
from CarChooser.Scrapper.serializer import Serializer
from CarChooser.Configs.logger import Logger
from CarChooser.Configs.config_reader import get_config

from CarChooser.RestApi import api_runner


def start():
    argument_list = sys.argv[1:]
    log = Logger().custom_logger()
    if argument_list:
        query = Query(log)
        serializer = Serializer(log)
        for argument in argument_list:
            if argument == '-AutoRia':
                config = get_config('AutoRia')
                ria_parser.run(log, config, query, serializer)
            elif argument == 'runserver':
                api_runner.runserver()
            else:
                log.error(f"Can not find your argument: {argument}")
    else:
        log.error(f'With run command u must to pass the one of arguments: ["-AutoRia"]')


if __name__ == '__main__':
    start()
