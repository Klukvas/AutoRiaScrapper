from pathlib import Path
import os
import configparser
ROOT_DIRECTORY = Path(__file__).parent.parent.parent.parent

def find_file(searched_name: str, search_for_file=True):
    for root, dirs, files in os.walk(ROOT_DIRECTORY, topdown=True):
        dirs[:] = [dir for dir in dirs if dir != ".venv"]
        for name in files if search_for_file else dirs:
            if name == searched_name:
                return os.path.join(root, name)
        

def change_alembic_ini(path_to_config: str, path_to_migrations_folder: str):
    config = configparser.ConfigParser()
    config.read(path_to_config)
    if not config['alembic']['script_location']:
        raise FileNotFoundError(f"Can not find script_location in file({path_to_config})")
    config.set('alembic','script_location', path_to_migrations_folder)
    with open(path_to_config, 'w') as configfile:
        config.write(configfile)
    return 0
if __name__ == "__main__":
    change_alembic_ini(
        str(Path(r"/Users/apavlenko/Desktop/AutoRiaScrapper/CarChooser/Scrapper/alembic.ini")),
        "121221122112"
        )