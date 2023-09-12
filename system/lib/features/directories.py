import os
import shutil


def create_directories():
    for io_type in ("In", "Out"):
        for filetype in ("Compressed", "Decompressed", "Sprites"):
            os.makedirs(f"SC/{io_type}-{filetype}", exist_ok=True)

        for filetype in ("Compressed", "Decompressed"):
            os.makedirs(f"CSV/{io_type}-{filetype}", exist_ok=True)

        for filetype in ("KTX", "PNG"):
            os.makedirs(f"TEX/{io_type}-{filetype}", exist_ok=True)


def clear_directories():
    for io_type in ("In", "Out"):
        for filetype in ("Compressed", "Decompressed", "Sprites"):
            folder = f"SC/{io_type}-{filetype}"
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)

        for filetype in ("Compressed", "Decompressed"):
            folder = f"CSV/{io_type}-{filetype}"
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)

        for filetype in ("KTX", "PNG"):
            folder = f"TEX/{io_type}-{filetype}"
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
