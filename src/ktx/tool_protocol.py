from pathlib import Path
from typing import Protocol


class KtxToolProtocol(Protocol):
    @classmethod
    def is_available(cls) -> bool: ...

    @classmethod
    def convert_ktx_to_png(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path: ...

    @classmethod
    def convert_png_to_ktx(
        cls, filepath: Path, output_folder: Path | None = None
    ) -> Path: ...
