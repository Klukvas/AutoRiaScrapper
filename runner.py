from AutoRia import ria_parser
import  sys
from logger import Logger
from ParkDrive import drive_parser

def start():
    log = Logger().custom_logger()
    argumentList = sys.argv[1:]
    if argumentList:
        for argument in argumentList:
            if argument == '-AutoRia':
                ria_parser.run(log)
            elif argument == '-ParkDrive':
                drive_parser.run()
    else:
        log.error(f'With run command u must to pass the one of arguments: ["-AutoRia"]')
        




if __name__ == '__main__':
    start()