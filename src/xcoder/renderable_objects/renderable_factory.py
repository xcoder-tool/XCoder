from sc import MovieClip, Shape, SupercellSWF, SwfObject, TextField

from .display_object import DisplayObject
from .renderable_movie_clip import RenderableMovieClip
from .renderable_shape import RenderableShape


def create_renderable_from_plain(
    swf: SupercellSWF, original_object: SwfObject
) -> DisplayObject:
    if isinstance(original_object, Shape):
        return RenderableShape(original_object)
    if isinstance(original_object, TextField):
        raise Exception("TextFields are not supported yet")
        # return RenderableTextField(original_object)
    if isinstance(original_object, MovieClip):
        children: list[DisplayObject] = []

        for child in original_object.children:
            bind_object = swf.get_display_object(child.id)
            assert bind_object is not None

            display_object = create_renderable_from_plain(swf, bind_object)
            display_object.set_blend_mode(child.blend & 63)
            display_object.set_visible(child.blend & 64 != 0)

            children.append(display_object)

        return RenderableMovieClip.create_from_plain(swf, original_object, children)

    raise Exception(f"Unsupported object type: {original_object}")
