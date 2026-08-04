import os
from pathlib import Path

from sc import Matrix2x3, SupercellSWF

from xcoder.config import config
from xcoder.console import Console
from xcoder.localization import locale

from ..renderable_objects import create_renderable_from_plain


def render_objects(swf: SupercellSWF, output_folder: Path) -> None:
    os.makedirs(output_folder / "overwrite", exist_ok=True)
    os.makedirs(output_folder / "shapes", exist_ok=True)
    os.makedirs(output_folder / "movie_clips", exist_ok=True)

    shape_count = len(swf.shapes)

    for shape_index, shape in enumerate(swf.shapes):
        Console.progress_bar(
            locale.cut_sprites_process % (shape_index + 1, shape_count),
            shape_index,
            shape_count,
        )

        rendered_shape = create_renderable_from_plain(swf, shape).render(Matrix2x3())
        rendered_shape.save(f"{output_folder}/shapes/{shape.id}.png")

        for region_index, command in enumerate(shape.commands):
            rendered_region = command.get_image()
            rendered_region.save(f"{output_folder}/shape_{shape.id}_{region_index}.png")

    if config.should_render_movie_clips:
        movie_clips_skipped = 0
        movie_clip_count = len(swf.movie_clips)
        for movie_clip_index in range(movie_clip_count):
            movie_clip = swf.movie_clips[movie_clip_index]

            rendered_movie_clip = create_renderable_from_plain(swf, movie_clip).render(
                Matrix2x3()
            )
            if sum(rendered_movie_clip.size) >= 2:
                clip_name = movie_clip.export_name or movie_clip.id
                rendered_movie_clip.save(f"{output_folder}/movie_clips/{clip_name}.png")
            else:
                # For debug:
                # logger.warning(f'MovieClip {movie_clip.id} cannot be rendered.')
                movie_clips_skipped += 1

            Console.progress_bar(
                "Rendering movie clips (%d/%d). Skipped count: %d"
                % (movie_clip_index + 1, movie_clip_count, movie_clips_skipped),
                movie_clip_index,
                movie_clip_count,
            )
