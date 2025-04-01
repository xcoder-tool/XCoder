from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xcoder.swf import SupercellSWF


class PlainObject(ABC):
    @abstractmethod
    def load(self, swf: SupercellSWF, tag: int):
        ...
