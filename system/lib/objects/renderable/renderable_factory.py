from system.lib.objects import Shape
from system.lib.objects.movie_clip.movie_clip import MovieClip
from system.lib.objects.plain_object import PlainObject
from system.lib.objects.renderable.display_object import DisplayObject
from system.lib.objects.renderable.renderable_movie_clip import RenderableMovieClip
from system.lib.objects.renderable.renderable_shape import RenderableShape
from system.lib.swf import SupercellSWF


def create_renderable_from_plain(
    swf: SupercellSWF, plain_object: PlainObject
) -> DisplayObject:
    if isinstance(plain_object, Shape):
        return RenderableShape(plain_object)
    if isinstance(plain_object, MovieClip):
        children = []

        for bind_id in plain_object.binds:
            bind_object = swf.get_display_object(bind_id)

            display_object = None
            if bind_object is not None:
                display_object = create_renderable_from_plain(swf, bind_object)

            children.append(display_object)

        return RenderableMovieClip.create_from_plain(swf, plain_object, children)

    raise Exception(f"Unsupported object type: {plain_object}")
