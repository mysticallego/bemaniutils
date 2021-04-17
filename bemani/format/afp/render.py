from typing import Dict, List, Tuple, Optional
from PIL import Image  # type: ignore

from .swf import SWF, Frame, Tag, AP2ShapeTag, AP2DefineSpriteTag, AP2PlaceObjectTag, AP2RemoveObjectTag, AP2DoActionTag, AP2DefineFontTag, AP2DefineEditTextTag
from .types import Color, Matrix, Point
from .geo import Shape
from .util import VerboseOutput


class Clip:
    # A movie clip that we are rendering, frame by frame. These are manifest by the root
    # SWF as well as AP2DefineSpriteTags which are essentially embedded movie clips.
    def __init__(self, tag_id: Optional[int], frames: List[Frame], tags: List[Tag]) -> None:
        self.tag_id = tag_id
        self.frames = frames
        self.tags = tags
        self.frameno = 0

    @property
    def frame(self) -> Frame:
        # The current frame object.
        if self.finished:
            raise Exception("Logic error!")
        return self.frames[self.frameno]

    def advance(self) -> None:
        # Advance the clip by one frame after we finished processing that frame.
        if not self.finished:
            self.frameno += 1

    @property
    def finished(self) -> bool:
        # Whether we've hit the end of the clip or not.
        return self.frameno == len(self.frames)

    @property
    def running(self) -> bool:
        # Whether we are still running.
        return self.frameno < len(self.frames)

    def __repr__(self) -> str:
        return f"Clip(tag_id={self.tag_id}, frames={len(self.frames)}, frameno={self.frameno})"


class PlacedObject:
    # An object that occupies the screen at some depth. Placed by an AP2PlaceObjectTag
    # that is inside the root SWF or an AP2DefineSpriteTag (essentially an embedded
    # movie clip).
    def __init__(self, parent_clip: Optional[int], tag: AP2PlaceObjectTag) -> None:
        self.parent_clip = parent_clip
        self.tag = tag

    @property
    def depth(self) -> int:
        return self.tag.depth

    @property
    def object_id(self) -> int:
        return self.tag.object_id

    def __repr__(self) -> str:
        return f"PlacedObject(parent_clip={self.parent_clip}, object_id={self.object_id}, depth={self.depth})"


class AFPRenderer(VerboseOutput):
    def __init__(self, shapes: Dict[str, Shape] = {}, textures: Dict[str, Image.Image] = {}, swfs: Dict[str, SWF] = {}) -> None:
        super().__init__()

        self.shapes: Dict[str, Shape] = shapes
        self.textures: Dict[str, Image.Image] = textures
        self.swfs: Dict[str, SWF] = swfs

        # Internal render parameters
        self.__visible_tag: Optional[int] = None
        self.__registered_shapes: Dict[int, Shape] = {}
        self.__placed_objects: List[PlacedObject] = []

    def add_shape(self, name: str, data: Shape) -> None:
        # Register a named shape with the renderer.
        if not data.parsed:
            data.parse()
        self.shapes[name] = data

    def add_texture(self, name: str, data: Image.Image) -> None:
        # Register a named texture (already loaded PIL image) with the renderer.
        self.textures[name] = data

    def add_swf(self, name: str, data: SWF) -> None:
        # Register a named SWF with the renderer.
        if not data.parsed:
            data.parse()
        self.swfs[name] = data

    def render_path(self, path: str, verbose: bool = False) -> Tuple[int, List[Image.Image]]:
        # Given a path to a SWF root animation or an exported animation inside a SWF,
        # attempt to render it to a list of frames, one per image.
        components = path.split(".")

        if len(components) > 2:
            raise Exception('Expected a path in the form of "moviename" or "moviename.exportedtag"!')

        for name, swf in self.swfs.items():
            if swf.exported_name == components[0]:
                # This is the SWF we care about.
                with self.debugging(verbose):
                    return self.__render(swf, components[1] if len(components) > 1 else None)

        raise Exception(f'{path} not found in registered SWFs!')

    def list_paths(self, verbose: bool = False) -> List[str]:
        # Given the loaded animations, return a list of possible paths to render.
        paths: List[str] = []

        for name, swf in self.swfs.items():
            paths.append(swf.exported_name)

            for export_tag in swf.exported_tags:
                paths.append(f"{swf.exported_name}.{export_tag}")

        return paths

    def __place(self, tag: Tag, parent_clip: Optional[int], prefix: str = "") -> List[Clip]:
        # "Place" a tag on the screen. Most of the time, this means performing the action of the tag,
        # such as defining a shape (registering it with our shape list) or adding/removing an object.
        if isinstance(tag, AP2ShapeTag):
            self.vprint(f"{prefix}    Loading {tag.reference} into shape slot {tag.id}")

            if tag.reference not in self.shapes:
                raise Exception(f"Cannot find shape reference {tag.reference}!")
            if tag.id in self.__registered_shapes:
                raise Exception(f"Cannot register {tag.reference} as shape slot {tag.id} is already taken!")

            self.__registered_shapes[tag.id] = self.shapes[tag.reference]

            # No additional movie clips were spawned.
            return []
        elif isinstance(tag, AP2DefineSpriteTag):
            self.vprint(f"{prefix}    Registering Sprite Tag {tag.id}")

            # Register a new clip that we have to execute.
            clip = Clip(tag.id, tag.frames, tag.tags)
            clips: List[Clip] = [clip]

            # Now, we need to run the first frame of this clip, since that's this frame.
            if clip.running:
                if clip.frame.num_tags > 0:
                    self.vprint(f"{prefix}      First Frame Initialization, Start Frame: {clip.frame.start_tag_offset}, Num Frames: {clip.frame.num_tags}")
                    for child in clip.tags[clip.frame.start_tag_offset:(clip.frame.start_tag_offset + clip.frame.num_tags)]:
                        clips.extend(self.__place(child, parent_clip=tag.id, prefix=prefix + "    "))

            # Finally, return the new clips we registered, including any that were done
            # in recursive calls to __place.
            return clips
        elif isinstance(tag, AP2PlaceObjectTag):
            if tag.update:
                self.vprint(f"{prefix}    Updating Object ID {tag.object_id} on Depth {tag.depth}")
                updated = False

                for obj in self.__placed_objects:
                    if obj.object_id == tag.object_id and obj.depth == tag.depth:
                        # As far as I can tell, pretty much only color and matrix stuff can be updated.
                        obj.tag.mult_color = tag.mult_color or obj.tag.mult_color
                        obj.tag.add_color = tag.add_color or obj.tag.add_color
                        obj.tag.transform = tag.transform or obj.tag.transform
                        obj.tag.rotation_offset = tag.rotation_offset or obj.tag.rotation_offset
                        updated = True

                if not updated:
                    raise Exception(f"Couldn't find tag {tag.object_id} on depth {tag.depth} to update!")
            else:
                self.vprint(f"{prefix}    Placing Object ID {tag.object_id} onto Depth {tag.depth}")

                self.__placed_objects.append(PlacedObject(parent_clip, tag))

            # TODO: Handle ON_LOAD triggers for this object. Many of these are just calls into
            # the game to set the current frame that we're on, but sometimes its important.

            return []
        elif isinstance(tag, AP2RemoveObjectTag):
            self.vprint(f"{prefix}    Removing Object ID {tag.object_id} from Depth {tag.depth}")

            if tag.object_id != 0:
                # Remove the identified object by object ID and depth.
                old_len = len(self.__placed_objects)

                self.__placed_objects = [
                    obj for obj in self.__placed_objects
                    if not(obj.object_id == tag.object_id and obj.depth == tag.depth)
                ]

                # We should have removed at least one objct.
                if len(self.__placed_objects) == old_len:
                    raise Exception(f"Couldn't find object to remove by ID {tag.object_id} and depth {tag.depth}!")
            else:
                # Remove the last placed object at this depth. The placed objects list isn't
                # ordered so much as apppending to the list means the last placed object at a
                # depth comes last.
                for i in range(len(self.__placed_objects)):
                    real_index = len(self.__placed_objects) - (i + 1)

                    if self.__placed_objects[real_index].depth == tag.depth:
                        self.__placed_objects = self.__placed_objects[:real_index] + self.__placed_objects[(real_index + 1):]
                        break
                else:
                    raise Exception(f"Couldn't find a recently-placed object to remove on depth {tag.depth}!")

            return []
        elif isinstance(tag, AP2DoActionTag):
            print("WARNING: Unhandled DO_ACTION tag!")
            return []
        elif isinstance(tag, AP2DefineFontTag):
            print("WARNING: Unhandled DEFINE_FONT tag!")
            return []
        elif isinstance(tag, AP2DefineEditTextTag):
            print("WARNING: Unhandled DEFINE_EDIT_TEXT tag!")
            return []
        else:
            raise Exception(f"Failed to process tag: {tag}")

    def __render_object(self, img: Image.Image, tag: AP2PlaceObjectTag, parent_transform: Matrix, parent_origin: Point) -> Image.Image:
        if tag.source_tag_id is None:
            self.vprint("    Nothing to render!")
            return img

        # Double check supported options.
        if tag.mult_color or tag.add_color:
            print(f"WARNING: Unhandled color blend request Mult: {tag.mult_color} Add: {tag.add_color}!")

        # Look up the affine transformation matrix and rotation/origin.
        transform = tag.transform or Matrix.identity()
        origin = tag.rotation_offset or Point.identity()

        # TODO: Need to do actual affine transformations here.
        if transform.b != 0.0 or transform.c != 0.0 or transform.a != 1.0 or transform.d != 1.0:
            print("WARNING: Unhandled affine transformation request!")
        if parent_transform.b != 0.0 or parent_transform.c != 0.0 or parent_transform.a != 1.0 or parent_transform.d != 1.0:
            print("WARNING: Unhandled affine transformation request!")
        offset = parent_transform.multiply_point(transform.multiply_point(Point.identity().subtract(origin).subtract(parent_origin)))

        # Look up source shape.
        if tag.source_tag_id not in self.__registered_shapes:
            # This is probably a sprite placement reference.
            found_one = False
            for obj in self.__placed_objects:
                if obj.parent_clip == tag.source_tag_id:
                    self.vprint(f"    Rendering placed object ID {obj.object_id} from sprite {obj.parent_clip} onto Depth {obj.depth}")
                    img = self.__render_object(img, obj.tag, transform, origin)
                    found_one = True

            if not found_one:
                raise Exception(f"Couldn't find parent clip {obj.parent_clip} to render animation out of!")

            return img

        # This is a shape draw reference.
        shape = self.__registered_shapes[tag.source_tag_id]

        for params in shape.draw_params:
            if not (params.flags & 0x1):
                # Not instantiable, don't render.
                return img

            if params.flags & 0x4 or params.flags & 0x8:
                # TODO: Need to support blending and UV coordinate colors here.
                print("WARNING: Unhandled shape blend or UV coordinate color!")

            texture = None
            if params.flags & 0x2:
                # We need to look up the texture for this.
                if params.region not in self.textures:
                    raise Exception(f"Cannot find texture reference {params.region}!")
                texture = self.textures[params.region]

            if texture is not None:
                # Now, render out the texture.
                cutin = Point(offset.x, offset.y)
                cutoff = Point.identity()
                if cutin.x < 0:
                    cutoff.x = -cutin.x
                    cutin.x = 0
                if cutin.y < 0:
                    cutoff.y = -cutin.y
                    cutin.y = 0

                img.alpha_composite(texture, cutin.as_tuple(), cutoff.as_tuple())
        return img

    def __render(self, swf: SWF, export_tag: Optional[str]) -> Tuple[int, List[Image.Image]]:
        # If we are rendering an exported tag, we want to perform the actions of the
        # rest of the SWF but not update any layers as a result.
        self.__visible_tag = None
        if export_tag is not None:
            # Make sure this tag is actually present in the SWF.
            if export_tag not in swf.exported_tags:
                raise Exception(f'{export_tag} is not exported by {swf.exported_name}!')
            self.__visible_tag = swf.exported_tags[export_tag]

        # TODO: We have to resolve imports.

        # Now, let's go through each frame, performing actions as necessary.
        spf = 1.0 / swf.fps
        frames: List[Image.Image] = []
        frameno: int = 0
        clips: List[Clip] = [Clip(None, swf.frames, swf.tags)] if len(swf.frames) > 0 else []

        # Reset any registered shapes.
        self.__registered_shapes = {}

        while any(c.running for c in clips):
            # Create a new image to render into.
            time = spf * float(frameno)
            color = swf.color or Color(0.0, 0.0, 0.0, 0.0)
            curimage = Image.new("RGBA", (swf.location.width, swf.location.height), color=color.as_tuple())
            self.vprint(f"Rendering Frame {frameno} ({time}s)")

            # Go through all registered clips, place all needed tags.
            newclips: List[Clip] = []
            for clip in clips:
                if clip.frame.num_tags > 0:
                    self.vprint(f"  Sprite Tag ID: {clip.tag_id}, Start Frame: {clip.frame.start_tag_offset}, Num Frames: {clip.frame.num_tags}")
                    for tag in clip.tags[clip.frame.start_tag_offset:(clip.frame.start_tag_offset + clip.frame.num_tags)]:
                        newclips.extend(self.__place(tag, parent_clip=clip.tag_id))

            # Add any new clips that we should process next frame.
            clips.extend(newclips)

            # Now, render out the placed objects. We sort by depth so that we can
            # get the layering correct, but its important to preserve the original
            # insertion order for delete requests.
            for obj in sorted(self.__placed_objects, key=lambda obj: obj.depth):
                if self.__visible_tag != obj.parent_clip:
                    continue

                self.vprint(f"  Rendering placed object ID {obj.object_id} from sprite {obj.parent_clip} onto Depth {obj.depth}")
                curimage = self.__render_object(curimage, obj.tag, Matrix.identity(), Point.identity())

            # Advance all the clips and frame now that we processed and rendered them.
            for clip in clips:
                clip.advance()
            frames.append(curimage)
            frameno += 1

            # Garbage collect any clips that we're finished with.
            clips = [c for c in clips if c.running]

        return int(spf * 1000.0), frames