import os
from pathlib import Path

from xcoder.config import config
from xcoder.console import Console
from xcoder.localization import locale
from xcoder.matrices import Matrix2x3
from xcoder.objects.renderable.renderable_factory import create_renderable_from_plain
from xcoder.swf import SupercellSWF


def render_objects(swf: SupercellSWF, output_folder: Path):
    os.makedirs(output_folder / "overwrite", exist_ok=True)
    os.makedirs(output_folder / "shapes", exist_ok=True)
    os.makedirs(output_folder / "movie_clips", exist_ok=True)

    shapes_count = len(swf.shapes)

    swf.xcod_writer.write_uint16(shapes_count)
    for shape_index in range(shapes_count):
        shape = swf.shapes[shape_index]

        regions_count = len(shape.regions)
        swf.xcod_writer.write_uint16(shape.id)
        swf.xcod_writer.write_uint16(regions_count)
        for region_index in range(regions_count):
            region = shape.regions[region_index]

            swf.xcod_writer.write_ubyte(region.texture_index)
            swf.xcod_writer.write_ubyte(region.get_point_count())

            for i in range(region.get_point_count()):
                swf.xcod_writer.write_uint16(int(region.get_u(i)))
                swf.xcod_writer.write_uint16(int(region.get_v(i)))

    for shape_index in range(shapes_count):
        shape = swf.shapes[shape_index]

        Console.progress_bar(
            locale.cut_sprites_process % (shape_index + 1, shapes_count),
            shape_index,
            shapes_count,
        )

        rendered_shape = create_renderable_from_plain(swf, shape).render(Matrix2x3())
        rendered_shape.save(f"{output_folder}/shapes/{shape.id}.png")

        regions_count = len(shape.regions)
        for region_index in range(regions_count):
            region = shape.regions[region_index]

            rendered_region = region.get_image()
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
