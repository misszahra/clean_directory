import shutil
from pathlib import Path
from src.data import DATA_DIR
from src.utils.io import read_json
from loguru import logger
from typing import Union
import sys


class OrgenizeFiles:
    """This class is used to orgenize file in the directory by
       moving files in to directories based on mime type.
    """
    def __init__(self):
        ext_dir = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dir.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name
        # print(self.extensions_dest)

    def __call__(self, directory:Union[str, Path]):
        """Orgenize file in a deirectory by moving  them to
        sub directories based on extensoins
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} is not exists")
        logger.info(f"Orgenaizing file in {directory}...")
        file_extensions = []
        for file_path in directory.iterdir():

            # ignor directories
            if file_path.is_dir():
                continue

            # ignor hidden files
            if file_path.name.startswith('.'):
                continue

            # get all file type
            file_extensions.append(file_path.suffix)

            # moves files
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = self.directory / "other"
            else:
                DEST_DIR = self.directory / self.extensions_dest[file_path.suffix]
            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path.suffix:10} To {DEST_DIR}...")
            shutil.move(src=str(file_path), dst=str(DEST_DIR))


if __name__ == "__main__":
    org_files = OrgenizeFiles()
    org_files(sys.argv[1])
    print('Done!')
