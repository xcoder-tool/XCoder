import os
from pathlib import Path
import platform

# Put executable files in "src/ktx/bin"
_main_dir = Path(__file__).parent
bin_dir = _main_dir / "bin"


# Note: a solution from
# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def get_executable_path(
    *paths: os.PathLike[str] | str,
) -> os.PathLike[str] | str | None:
    from shutil import which

    for path in paths:
        # Fix of https://github.com/xcoder-tool/XCoder/issues/22
        executable_path = which(path)
        if executable_path is not None:
            return path

    return None


is_windows = platform.system() == "Windows"
null_output = f"{'nul' if is_windows else '/dev/null'} 2>&1"


def run(command: str, output_path: str = null_output) -> int:
    return os.system(f"{command} > {output_path}")
