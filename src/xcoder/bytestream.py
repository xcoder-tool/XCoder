import io
import struct
from typing import Literal


class Reader:
    def __init__(
        self,
        initial_buffer: bytes = b"",
        endian: Literal["little", "big"] = "little",
    ):
        self._internal_reader = io.BytesIO(initial_buffer)

        self.endian: Literal["little", "big"] = endian
        self.endian_sign: Literal["<", ">"] = "<" if endian == "little" else ">"

    def seek(self, position: int) -> None:
        self._internal_reader.seek(position)

    def tell(self) -> int:
        return self._internal_reader.tell()

    def read(self, size: int) -> bytes:
        return self._internal_reader.read(size)

    def read_uchar(self) -> int:
        return struct.unpack("B", self.read(1))[0]

    def read_char(self) -> int:
        return struct.unpack("b", self.read(1))[0]

    def read_ushort(self) -> int:
        return struct.unpack(f"{self.endian_sign}H", self.read(2))[0]

    def read_short(self) -> int:
        return struct.unpack(f"{self.endian_sign}h", self.read(2))[0]

    def read_uint(self) -> int:
        return struct.unpack(f"{self.endian_sign}I", self.read(4))[0]

    def read_int(self) -> int:
        return struct.unpack(f"{self.endian_sign}i", self.read(4))[0]

    def read_twip(self) -> float:
        return self.read_int() / 20

    def read_string(self) -> str:
        length = self.read_uchar()
        if length != 0xFF:
            return self.read(length).decode()
        return ""


class Writer(io.BytesIO):
    def __init__(self, endian: Literal["little", "big"] = "little"):
        super().__init__()
        self._endian: Literal["little", "big"] = endian

    def write_int(self, integer: int, length: int = 1, signed: bool = False):
        self.write(integer.to_bytes(length, self._endian, signed=signed))

    def write_ubyte(self, integer: int):
        self.write_int(integer)

    def write_byte(self, integer: int):
        self.write_int(integer, signed=True)

    def write_uint16(self, integer: int):
        self.write_int(integer, 2)

    def write_int16(self, integer: int):
        self.write_int(integer, 2, True)

    def write_uint32(self, integer: int):
        self.write_int(integer, 4)

    def write_int32(self, integer: int):
        self.write_int(integer, 4, True)

    def write_string(self, string: str | None = None):
        if string is None:
            self.write_byte(0xFF)
            return

        encoded = string.encode()
        self.write_byte(len(encoded))
        self.write(encoded)
