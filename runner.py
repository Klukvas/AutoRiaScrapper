from CarChooser.Scrapper.AutoRia import ria_parser
from CarChooser.Scrapper.query import Query
from CarChooser.Scrapper.serializer import Serializer
import sys
from CarChooser.Configs.logger import Logger
from CarChooser.Configs.config_reader import get_config
print('asd')

def start():
    argumentList = ['-AutoRia']
    log = Logger().custom_logger()
    if argumentList:
        print('asd21')
        query = Query(log)
        print(12)
        serializer = Serializer(log)
        print('asd1231231')

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
