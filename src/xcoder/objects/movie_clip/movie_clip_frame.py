from xcoder.bytestream import Reader


class MovieClipFrame:
    def __init__(self):
        self._elements_count: int = 0
        self._label: str | None = None

        self._elements: list[tuple[int, int, int]] = []

    def load(self, reader: Reader) -> None:
        self._elements_count = reader.read_short()
        self._label = reader.read_string()

    def get_elements_count(self) -> int:
        return self._elements_count

    def set_elements(self, elements: list[tuple[int, int, int]]) -> None:
        self._elements = elements

    def get_elements(self) -> list[tuple[int, int, int]]:
        return self._elements

    def get_element(self, index: int) -> tuple[int, int, int]:
        return self._elements[index]
