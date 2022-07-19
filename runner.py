from Scrapper.AutoRia import ria_parser
from Scrapper.query import Query
from Scrapper.serializer import Serializer
import sys
from logger import Logger
from config_reader import get_config


def start():
    argumentList = sys.argv[1:]
    log = Logger().custom_logger()
    if argumentList:
        query = Query(log)
        serializer = Serializer(log)
        for argument in argumentList:
            if argument == '-AutoRia':
                config = get_config('AutoRia')
                ria_parser.run(log, config, query, serializer)
            else:
                log.error(f"Can not find your argument: {argument}")
    else:
        log.error(f'With run command u must to pass the one of arguments: ["-AutoRia"]')


if __name__ == '__main__':
    start()
