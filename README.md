# XCoder - easy to use modding tool

Multiplatform modding tool for ANY Supercell\`s game.

## About

Work with Supercell\`s files on **any** os! SC and CSV are supported for all
Supercell\`s games.

### Features:

- SC compile / decompile
- Compression and decompression

### How to install and use

- On Windows:
    - Download Python 3.10 or newer version
      from [official page](https://www.python.org/downloads/)
    - Install Python. While Installing, enable such parameters as "Add Python to
      PATH", "Install pip", "Install py launcher", "Associate files with Python" and "Add Python to environment variables"
    - Download XCoder from the [releases page](https://github.com/xcoder-tool/XCoder/releases) and extract it
    - Locate the extracted directory and install required modules:
      ```cmd
      poetry install
      ```
    - Run program with 
      ```cmd
      poetry run python -m xcoder
      ```

- On Linux:
  - Open Terminal and install Python by executing following command:
    ```sh
    sudo apt-get update && sudo apt-get install python3 python3-poetry
    ```
  - Download XCoder from the [releases page](https://github.com/xcoder-tool/XCoder/releases) and extract it
  - Locate the extracted directory and install required modules by executing following
  command:
    ```sh
    poetry install
    ```
  - Run program with
    ```cmd
    poetry run python -m xcoder
    ```

### Testing

The project supports unit-testing using the unittest module. To run tests by yourself,
use the command:

```sh
poetry run python -m unittest
```

### How to enable KTX section

![KTX section demo](docs/KTX%20section.png)

**Supercell also uses KTX textures in new versions of the games, so it is advisable to
perform this step.**

To enable the KTX module, you need to get the "PVRTexToolCLI" binary from the official
site: https://developer.imaginationtech.com/pvrtextool/.

Then it is necessary to put CLI in "bin/" folder in the main script folder.

### In the plans:

- CSV updating.

## Credits

This tool is based on Original [XCoder](https://github.com/MasterDevX/xcoder),
Developer: [MasterDevX](https://github.com/MasterDevX)</br>

Many thanks to [spiky_Spike](https://github.com/spiky-s) for the provided developments
