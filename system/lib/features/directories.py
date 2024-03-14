import os
import shutil

IO_TYPES = ("In", "Out")

SC_FILE_TYPES = ("Compressed", "Decompressed", "Sprites")
CSV_FILE_TYPES = ("Compressed", "Decompressed")
TEXTURE_FILE_TYPES = ("KTX", "PNG")


def create_directories():
    for io_type in IO_TYPES:
        for filetype in SC_FILE_TYPES:
            os.makedirs(f"SC/{io_type}-{filetype}", exist_ok=True)

        for filetype in CSV_FILE_TYPES:
            os.makedirs(f"CSV/{io_type}-{filetype}", exist_ok=True)

        for filetype in TEXTURE_FILE_TYPES:
            os.makedirs(f"TEX/{io_type}-{filetype}", exist_ok=True)


def clear_directories():
    for io_type in IO_TYPES:
        for filetype in SC_FILE_TYPES:
            _recreate_directory(f"SC/{io_type}-{filetype}")

        for filetype in CSV_FILE_TYPES:
            _recreate_directory(f"CSV/{io_type}-{filetype}")

        for filetype in TEXTURE_FILE_TYPES:
            _recreate_directory(f"TEX/{io_type}-{filetype}")


def _recreate_directory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)
