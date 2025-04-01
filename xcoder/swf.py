import os
from pathlib import Path

from loguru import logger
from sc_compression import Signatures

from xcoder.bytestream import Reader, Writer
from xcoder.features.files import open_sc
from xcoder.localization import locale
from xcoder.matrices.matrix_bank import MatrixBank
from xcoder.objects import MovieClip, Shape, SWFTexture
from xcoder.objects.plain_object import PlainObject

DEFAULT_HIGHRES_SUFFIX = "_highres"
DEFAULT_LOWRES_SUFFIX = "_lowres"


class SupercellSWF:
    TEXTURES_TAGS = (1, 16, 28, 29, 34, 19, 24, 27, 45, 47)
    SHAPES_TAGS = (2, 18)
    MOVIE_CLIPS_TAGS = (3, 10, 12, 14, 35, 49)

    TEXTURE_EXTENSION = "_tex.sc"

    def __init__(self):
        self.filename: str | None = None
        self.reader: Reader | None = None

        self.use_lowres_texture: bool = False

        self.shapes: list[Shape] = []
        self.movie_clips: list[MovieClip] = []
        self.textures: list[SWFTexture] = []

        self.xcod_writer = Writer("big")

        self._filepath: Path | None = None
        self._uncommon_texture_path: os.PathLike | str | None = None

        self._lowres_suffix: str = DEFAULT_LOWRES_SUFFIX
        self._highres_suffix: str = DEFAULT_HIGHRES_SUFFIX

        self._use_uncommon_texture: bool = False

        self._shape_count: int = 0
        self._movie_clip_count: int = 0
        self._texture_count: int = 0
        self._text_field_count: int = 0

        self._export_count: int = 0
        self._export_ids: list[int] = []
        self._export_names: list[str] = []

        self._matrix_banks: list[MatrixBank] = []
        self._matrix_bank: MatrixBank | None = None

    def load(self, filepath: str | os.PathLike) -> tuple[bool, Signatures]:
        self._filepath = Path(filepath)

        texture_loaded, signature = self._load_internal(
            self._filepath, self._filepath.name.endswith("_tex.sc")
        )

        if not texture_loaded:
            if self._use_uncommon_texture:
                assert self._uncommon_texture_path is not None
                texture_loaded, signature = self._load_internal(
                    self._uncommon_texture_path, True
                )
            else:
                texture_path = str(self._filepath)[:-3] + SupercellSWF.TEXTURE_EXTENSION
                texture_loaded, signature = self._load_internal(texture_path, True)

        return texture_loaded, signature

    def _load_internal(
        self, filepath: os.PathLike | str, is_texture_file: bool
    ) -> tuple[bool, Signatures]:
        self.filename = os.path.basename(filepath)

        logger.info(locale.collecting_inf % self.filename)

        decompressed_data, signature, version = open_sc(filepath)

        if signature.name != Signatures.NONE:
            logger.info(locale.detected_comp % signature.name.upper())
        print()

        self.reader = Reader(decompressed_data)
        del decompressed_data

        if not is_texture_file:
            self._shape_count = self.reader.read_ushort()
            self._movie_clip_count = self.reader.read_ushort()
            self._texture_count = self.reader.read_ushort()
            self._text_field_count = self.reader.read_ushort()

            matrix_count = self.reader.read_ushort()
            color_transformation_count = self.reader.read_ushort()

            self._matrix_bank = MatrixBank()
            self._matrix_bank.init(matrix_count, color_transformation_count)
            self._matrix_banks.append(self._matrix_bank)

            self.shapes = [_class() for _class in [Shape] * self._shape_count]
            self.movie_clips = [
                _class() for _class in [MovieClip] * self._movie_clip_count
            ]
            self.textures = [_class() for _class in [SWFTexture] * self._texture_count]

            self.reader.read_uint()
            self.reader.read_char()

            self._export_count = self.reader.read_ushort()

            self._export_ids = []
            for _ in range(self._export_count):
                self._export_ids.append(self.reader.read_ushort())

            self._export_names = []
            for _ in range(self._export_count):
                self._export_names.append(self.reader.read_string())

        loaded = self._load_tags(is_texture_file)

        for i in range(self._export_count):
            export_id = self._export_ids[i]
            export_name = self._export_names[i]

            movie_clip = self.get_display_object(
                export_id, export_name, raise_error=True
            )

            if isinstance(movie_clip, MovieClip):
                movie_clip.export_name = export_name

        return loaded, signature

    def _load_tags(self, is_texture_file: bool) -> bool:
        assert self.reader is not None

        has_texture = True

        texture_id = 0
        movie_clips_loaded = 0
        shapes_loaded = 0
        matrices_loaded = 0

        while True:
            tag = self.reader.read_char()
            length = self.reader.read_uint()

            if tag == 0:
                return has_texture
            elif tag in SupercellSWF.TEXTURES_TAGS:
                # this is done to avoid loading the data file
                # (although it does not affect the speed)
                if is_texture_file and texture_id >= len(self.textures):
                    self.textures.append(SWFTexture())

                texture = self.textures[texture_id]
                texture.load(self, tag, has_texture)

                if has_texture:
                    logger.info(
                        locale.about_sc
                        % (
                            self.filename,
                            texture_id,
                            texture.pixel_type,
                            texture.width,
                            texture.height,
                        )
                    )
                    print()

                    self.xcod_writer.write_ubyte(tag)
                    self.xcod_writer.write_ubyte(texture.pixel_type)
                    self.xcod_writer.write_uint16(texture.width)
                    self.xcod_writer.write_uint16(texture.height)
                texture_id += 1
            elif tag in SupercellSWF.SHAPES_TAGS:
                self.shapes[shapes_loaded].load(self, tag)
                shapes_loaded += 1
            elif tag in SupercellSWF.MOVIE_CLIPS_TAGS:  # MovieClip
                self.movie_clips[movie_clips_loaded].load(self, tag)
                movie_clips_loaded += 1
            elif tag == 8 or tag == 36:  # Matrix
                assert self._matrix_bank is not None
                self._matrix_bank.get_matrix(matrices_loaded).load(self.reader, tag)
                matrices_loaded += 1
            elif tag == 26:
                has_texture = False
            elif tag == 30:
                self._use_uncommon_texture = True
                highres_texture_path = (
                    str(self._filepath)[:-3]
                    + self._highres_suffix
                    + SupercellSWF.TEXTURE_EXTENSION
                )
                lowres_texture_path = (
                    str(self._filepath)[:-3]
                    + self._lowres_suffix
                    + SupercellSWF.TEXTURE_EXTENSION
                )

                self._uncommon_texture_path = highres_texture_path
                if not os.path.exists(highres_texture_path) and os.path.exists(
                    lowres_texture_path
                ):
                    self._uncommon_texture_path = lowres_texture_path
                    self.use_lowres_texture = True
            elif tag == 42:
                matrix_count = self.reader.read_ushort()
                color_transformation_count = self.reader.read_ushort()

                self._matrix_bank = MatrixBank()
                self._matrix_bank.init(matrix_count, color_transformation_count)
                self._matrix_banks.append(self._matrix_bank)

                matrices_loaded = 0
            else:
                self.reader.read(length)

    def get_display_object(
        self, target_id: int, name: str | None = None, *, raise_error: bool = False
    ) -> PlainObject | None:
        for shape in self.shapes:
            if shape.id == target_id:
                return shape

        for movie_clip in self.movie_clips:
            if movie_clip.id == target_id:
                return movie_clip

        if raise_error:
            exception_text = (
                f"Unable to find some DisplayObject id {target_id}, {self.filename}"
            )
            if name is not None:
                exception_text += f" needed by export name {name}"

            raise ValueError(exception_text)
        return None

    def get_matrix_bank(self, index: int) -> MatrixBank:
        return self._matrix_banks[index]

    @property
    def filepath(self) -> Path:
        assert self._filepath is not None
        return self._filepath
