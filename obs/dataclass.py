from dataclasses import dataclass, field
from typing import Dict, Any
import obsws_python as obs


@dataclass
class SceneItemTransform:
    sourceWidth: int
    sourceHeight: int
    positionX: float
    positionY: float

    @staticmethod
    def from_response(response: Any) -> "SceneItemTransform":
        try:
            sceneItemTransform = getattr(response, "scene_item_transform")
            # sceneItemTransform is dict
            return SceneItemTransform(
                sourceWidth=sceneItemTransform.get("sourceWidth"),
                sourceHeight=sceneItemTransform.get("sourceHeight"),
                positionX=sceneItemTransform.get("positionX"),
                positionY=sceneItemTransform.get("positionY"),
            )
        except AttributeError:
            raise ValueError("Invalid response from SceneItemTransform")
