# XCoder - easy to use modding tool

A multiplatform modding tool designed for ANY Supercell game.

## About

Effortlessly work with Supercell\`s game files! XCoder offers support for SC and CSV
formats across all Supercell games.

### Features

- SC compile / decompile
- Compression and decompression

### Installation and Usage

**Windows**:

1. Download Python 3.10 or newer version from
   the [official page](https://www.python.org/downloads/)
2. Install Python. While Installing, enable such parameters as "Add Python to
   PATH", "Install pip", "Install py launcher", "Associate files with Python" and "Add
   Python to environment variables"

**Linux**:

1. Open Terminal and install Python using:
    ```sh
    sudo apt-get update && sudo apt-get install python3 python3-poetry
    ```

**Common steps**:

1. Download XCoder from
   the [releases page](https://github.com/xcoder-tool/XCoder/releases) and extract it
2. Go to the extracted directory and install required modules by executing:
    ```sh
    poetry install
    ```
3. Run program with
    ```sh
    poetry run python -m xcoder
    ```

### How to enable KTX section

![KTX section demo](docs/KTX%20section.png)

**Supercell also uses KTX textures in new versions of the games, so it is advisable to
perform this step.**

To enable the KTX module, you need to get the "PVRTexToolCLI" binary from the official
site: https://developer.imaginationtech.com/pvrtextool/.

Then it is necessary to put CLI in "bin/" folder in the main script folder or add it to
your PATH environment variable.

### Planned Features

- CSV updating

## Credits

XCoder is based on the original [XCoder](https://github.com/MasterDevX/xcoder),
developed by [MasterDevX](https://github.com/MasterDevX).</br>
Special thanks to [spiky_Spike](https://github.com/spiky-s) for their contributions.
